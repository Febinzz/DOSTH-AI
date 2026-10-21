"""
============================================================
  CareMate - Module 04: Bilingual Voice Assistant
  ============================================================
  Supports Malayalam and English voice commands.

  Pipeline:
    1. Listen via microphone (SpeechRecognition)
    2. Try recognizing in Malayalam (ml-IN), fall back to English (en-IN)
    3. Send recognized text to Groq LLM (llama3) for intelligent response
    4. Convert response to speech using gTTS
    5. Play audio via pygame (or mpg321)

  Special Commands (handled locally, no LLM needed):
    "status"  / "സ്റ്റാറ്റസ്"   → Read system status
    "stop"    / "നിർത്തുക"      → Stop voice assistant
    "help"    / "സഹായം"         → List available commands
    "call"    / "വിളിക്കൂ"      → Send emergency Telegram message

  Run standalone:
    python voice_assistant.py

  Install dependencies:
    sudo apt install espeak portaudio19-dev
    pip install SpeechRecognition gTTS pygame groq --break-system-packages
============================================================
"""

import os
import sys
import time
import logging
import subprocess
import threading
import tempfile
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s [VOICE] %(message)s')
log = logging.getLogger(__name__)

try:
    import speech_recognition as sr
    from gtts import gTTS
    import pygame
except ImportError as e:
    log.error(f"Missing dependency: {e}")
    log.error("Install: pip install SpeechRecognition gTTS pygame --break-system-packages")
    sys.exit(1)

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    log.warning("Groq not installed. Using simple fallback responses.")


# ============================================================
SYSTEM_PROMPT = """You are CareMate, an AI companion for elderly people.
You speak in simple, warm, and friendly language.
Keep responses short (under 3 sentences).
When speaking Malayalam, use proper Malayalam script.
You help with: medication reminders, health questions, weather, general conversation.
If someone asks about an emergency, tell them help is being alerted.
Always be gentle, patient, and reassuring.
When a detected facial emotion is provided, actively use it to shape the empathy,
tone, and emotional support in your reply; do not treat it as an optional detail.
Respond to the user's words and request while also addressing the emotional need
suggested by the detected emotion. Acknowledge the feeling naturally when helpful,
without claiming the estimate is certain or making a diagnosis. The user's words
remain the source for facts and what they are asking for."""

MAX_PREVIOUS_MESSAGES = 5
FACE_DETECTION_RECENCY_SECONDS = 8
FACE_LOST_RESET_SECONDS = 12

LOCAL_COMMANDS = {
    "status": "All systems are functioning normally.",
    "സ്റ്റാറ്റസ്": "എല്ലാ സിസ്റ്റങ്ങളും ശരിയായി പ്രവർത്തിക്കുന്നു.",
    "stop": "__STOP__",
    "നിർത്തുക": "__STOP__",
    "help": "You can ask me anything. Say 'status' for system status, 'stop' to stop, or just talk to me!",
    "സഹായം": "നിങ്ങൾക്ക് എന്നോട് ഏതു ചോദ്യവും ചോദിക്കാം. സ്റ്റാറ്റസ്, സഹായം, അല്ലെങ്കിൽ സംഭാഷണം തുടരൂ!",
    "call caregiver": "__CALL__",
    "emergency": "__CALL__",
}


class VoiceAssistant:
    """
    Bilingual voice assistant for CareMate.
    Listens, understands, and responds in Malayalam or English.
    """

    def __init__(self, shared_state=None):
        """
        Args:
            shared_state: Optional SharedState object from full_system (for status info).
        """
        self.shared_state  = shared_state
        self.running       = False
        self.recognizer    = sr.Recognizer()
        self.groq_client   = None
        self.conversation  = []   # Multi-turn conversation history
        # Facial emotion detection — initialized only when needed
        self._emotion_pipeline = None
        self.last_detected_emotion = None
        self.last_detected_second_emotion = None
        self._face_detected_since = None
        self._last_face_seen_at = None
        self._last_communication_at = time.monotonic()
        self._checkin_prompted = False

        if os.name != "nt":
            try:
                pygame.mixer.init()
            except Exception as e:
                log.warning(f"pygame mixer init failed: {e}. Will use mpg321 fallback.")

        # Init Groq
        if GROQ_AVAILABLE and config.GROQ_API_KEY != "YOUR_GROQ_API_KEY_HERE":
            self.groq_client = Groq(api_key=config.GROQ_API_KEY)
            log.info("Groq LLM connected.")
        else:
            log.warning("Groq API key not set. Using rule-based fallback responses.")

    # ----------------------------------------------------------
    def start(self):
        """Calibrate mic and begin listening loop."""
        log.info("Calibrating microphone for ambient noise...")
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        log.info("Microphone ready.")

        self.speak("CareMate voice assistant is ready.")
        self.running = True
        log.info("Voice assistant started. Say something!")

        self._loop()
    
    def _log_to_dashboard(
        self, user_text, emotion, assistant_reply, second_emotion=None
    ):
        """Send a completed CareMate interaction to Flask."""
        token = os.environ.get("CAREMATE_DASHBOARD_TOKEN")

        if not token:
            log.warning("Dashboard token is not configured.")
            return

        try:
            response = requests.post(
                "http://127.0.0.1:5000/api/log-interaction",
                headers={"X-CareMate-Token": token},
                json={
                    "emotion": emotion,
                    "second_emotion": second_emotion,
                    "user_text": user_text,
                    "assistant_reply": assistant_reply,
                },
                timeout=2,
            )

            if response.status_code != 201:
                log.warning(
                    "Dashboard logging failed: HTTP %s",
                    response.status_code,
                )

        except requests.RequestException as e:
            log.warning("Could not reach dashboard: %s", e)

    # ----------------------------------------------------------
    def _loop(self):
        """Main listen → understand → respond loop."""
        try:
            while self.running:
                text = self._listen()
                if text:
                    self._last_communication_at = time.monotonic()
                    self._checkin_prompted = False
                    log.info(f"You said: {text}")
                    response = self._process(
                        text,
                        emotion=self.last_detected_emotion,
                        second_emotion=self.last_detected_second_emotion,
                    )
                    if response == "__STOP__":
                        self.speak("Stopping voice assistant. Take care.")
                        break
                    elif response == "__CALL__":
                        self._emergency_call()
                        self._last_communication_at = time.monotonic()
                    elif response:
                        self._log_to_dashboard(
                            user_text=text,
                            emotion=self.last_detected_emotion,
                            assistant_reply=response,
                            second_emotion=self.last_detected_second_emotion,
                        )
                        self.speak(response)
                        self._last_communication_at = time.monotonic()
                elif self._should_offer_checkin():
                    self._checkin_prompted = True
                    log.info("No speech for 15 seconds while a face is present; asking in Malayalam.")
                    self.speak("നിങ്ങൾ ഇവിടെ ഉണ്ടോ? നിങ്ങൾക്ക് സുഖമാണോ?", lang="ml")
        except KeyboardInterrupt:
            log.info("Interrupted.")
        finally:
            log.info("Voice assistant stopped.")
    def _get_emotion_pipeline(self):
        """Load the existing FER model once; never train or download weights."""
        if self._emotion_pipeline is not None:
            return self._emotion_pipeline

        try:
            import cv2  # Ensure OpenCV is installed

            face_root = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "face_emotion_module")
            )

            model_path = os.path.join(
                face_root, "models", "fer", "emotion_model.onnx"
            )

            if not os.path.isfile(model_path):
                log.warning("FER model not found: %s", model_path)
                return None

            # Match the import structure used by run_fer_webcam.py.
            if face_root not in sys.path:
                sys.path.insert(0, face_root)

            from modules.fer.pipeline import FacialEmotionPipeline

            self._emotion_pipeline = FacialEmotionPipeline(
                model_path=model_path
            )
            log.info("Existing facial emotion model loaded.")
            return self._emotion_pipeline

        except Exception as e:
            log.warning("Facial emotion detection unavailable: %s", e)
            return None

    def _emotion_camera_worker(
        self, pipeline, stop_event, emotions, lock, face_presence
    ):
        """
        Sample facial expressions during microphone recording only.
        This worker owns and releases its camera.
        """
        cap = None

        try:
            import cv2

            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

            if not cap.isOpened():
                cap.release()
                cap = cv2.VideoCapture(0)

            if not cap.isOpened():
                log.warning("Could not open webcam; continuing without emotion.")
                return

            while not stop_event.is_set():
                ok, frame = cap.read()

                if not ok:
                    time.sleep(0.03)
                    continue

                try:
                    result = pipeline.process_frame(
                        frame, enable_enhancement=True
                    )

                    if result.get("face_detected", False):
                        with lock:
                            face_presence["last_seen_at"] = time.monotonic()

                    # Ignore missing faces and frames during calibration.
                    if not result.get("face_detected", False):
                        continue

                    if not result.get("baseline_calibrated", False):
                        continue

                    if not result.get("is_confident", False):
                        continue

                    emotion = result.get("primary_emotion")

                    if not isinstance(emotion, str):
                        continue

                    emotion = emotion.strip().lower()

                    if not emotion or emotion in {
                        "unclear",
                        "expression unclear",
                        "calibrating",
                    }:
                        continue

                    with lock:
                        emotions.append(emotion)

                except Exception as e:
                    log.debug("Skipping invalid FER frame: %s", e)

        except Exception as e:
            log.warning("Webcam sampling failed: %s", e)

        finally:
            if cap is not None:
                cap.release()
    # ----------------------------------------------------------
    def _listen(self):
        """
        Record speech and sample facial expressions during that recording.
        Release the camera before speech recognition begins.
        """
        self.last_detected_emotion = None
        self.last_detected_second_emotion = None

        pipeline = self._get_emotion_pipeline()

        stop_event = threading.Event()
        emotions = []
        face_presence = {"last_seen_at": None}
        lock = threading.Lock()
        camera_thread = None
        audio = None

        if pipeline is not None:
            try:
                camera_thread = threading.Thread(
                    target=self._emotion_camera_worker,
                    args=(pipeline, stop_event, emotions, lock, face_presence),
                    daemon=True,
                )
                camera_thread.start()

            except Exception as e:
                log.warning("Could not start emotion sampling: %s", e)

        try:
            with sr.Microphone() as source:
                log.info("Listening...")
                audio = self.recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=8,
                )

        except sr.WaitTimeoutError:
            log.info("No speech detected.")
            return None

        except Exception as e:
            log.error("Microphone recording failed: %s", e)
            return None

        finally:
            # Stop and join the worker before recognition or speaking.
            stop_event.set()

            if camera_thread is not None:
                camera_thread.join()

            with lock:
                recorded_emotions = list(emotions)
                last_face_seen_at = face_presence["last_seen_at"]

            self._update_face_presence(last_face_seen_at)

            
            if recorded_emotions:
                counts = {}

                for emotion in recorded_emotions:
                    emotion = emotion.strip().lower()
                    counts[emotion] = counts.get(emotion, 0) + 1

                ranked_emotions = sorted(
                    counts.items(), key=lambda item: item[1], reverse=True
                )
                dominant = ranked_emotions[0][0]
                second_emotion = (
                    ranked_emotions[1][0] if len(ranked_emotions) > 1 else None
                )
                self.last_detected_emotion = dominant
                self.last_detected_second_emotion = second_emotion

                log.info(
                    "Emotions sent for response: %s, %s (%d frames; samples=%s)",
                    dominant,
                    second_emotion or "none",
                    len(recorded_emotions),
                    counts,
                )
            else:
                self.last_detected_emotion = None
                self.last_detected_second_emotion = None
                log.info("No reliable facial expression detected.")

        if audio is None:
            return None

        # The webcam has already been released before this point.
        try:
            text = self.recognizer.recognize_google(
                audio, language="ml-IN"
            )
            log.info("Recognized (Malayalam): %s", text)
            return text

        except sr.UnknownValueError:
            pass

        except sr.RequestError as e:
            log.error("Google Speech API error: %s", e)
            return None

        try:
            text = self.recognizer.recognize_google(
                audio, language="en-IN"
            )
            log.info("Recognized (English): %s", text)
            return text

        except sr.UnknownValueError:
            log.info("Speech not understood.")
            return None

        except sr.RequestError as e:
            log.error("Google Speech API error: %s", e)
            return None

    def _update_face_presence(self, last_face_seen_at, now=None):
        """Track a recently visible face and restart timing after a long gap."""
        now = time.monotonic() if now is None else now
        face_is_recent = (
            last_face_seen_at is not None
            and now - last_face_seen_at <= FACE_DETECTION_RECENCY_SECONDS
        )

        if face_is_recent:
            if (
                self._last_face_seen_at is None
                or now - self._last_face_seen_at > FACE_LOST_RESET_SECONDS
            ):
                self._face_detected_since = last_face_seen_at
                self._checkin_prompted = False
            self._last_face_seen_at = now
        elif (
            self._last_face_seen_at is not None
            and now - self._last_face_seen_at > FACE_LOST_RESET_SECONDS
        ):
            self._face_detected_since = None
            self._last_face_seen_at = None
            self._checkin_prompted = False

    def _should_offer_checkin(self, now=None):
        """Offer one Malayalam check-in after 15 seconds of face-visible silence."""
        now = time.monotonic() if now is None else now
        if (
            self._face_detected_since is None
            or self._last_face_seen_at is None
            or self._checkin_prompted
            or now - self._last_face_seen_at > FACE_LOST_RESET_SECONDS
        ):
            return False

        silence_started_at = max(
            self._face_detected_since,
            self._last_communication_at,
        )
        return now - silence_started_at >= 15

    # ----------------------------------------------------------
    def _process(self, text, emotion=None, second_emotion=None):
        """
        Determine response to user's text.
        1. Check local commands first (no network needed).
        2. Get LLM response if Groq is available.
        3. Fall back to simple rule-based reply.
        """
        text_lower = text.lower().strip()

        # Check local commands
        for keyword, response in LOCAL_COMMANDS.items():
            if keyword in text_lower:
                if response == "__STOP__":
                    return "__STOP__"
                if response == "__CALL__":
                    return "__CALL__"
                # Status command: enrich with live data
                if keyword in ("status", "സ്റ്റാറ്റസ്") and self.shared_state:
                    return self._build_status_response()
                return response

        # LLM response
        if self.groq_client:
            return self._llm_response(
                text, emotion=emotion, second_emotion=second_emotion
            )

        # Simple fallback
        return self._fallback_response(text_lower)

    # ----------------------------------------------------------
    def _llm_response(self, user_text, emotion=None, second_emotion=None):
        """Get response from Groq LLM."""
        if emotion:
            detected_emotions = f"Primary detected facial emotion: {emotion}."
            if second_emotion:
                detected_emotions += (
                    f" Secondary detected facial emotion: {second_emotion}."
                )
            message_content = (
                f"The user said: {user_text}\n"
                f"{detected_emotions}\n"
                "Use the detected emotion estimates to shape your response: "
                "include suitable empathy or emotional support and adapt your "
                "tone to them. Consider both when available, without assuming "
                "either is certain. Do not ignore them. Respond "
                "to the user's actual words and request; do not assume the "
                "emotions are certain or present them as a diagnosis."
            )
        else:
            message_content = user_text
        current_message = {
            "role": "user",
            "content": message_content,
        }
        recent_history = self.conversation[-MAX_PREVIOUS_MESSAGES:]

        try:
            resp = self.groq_client.chat.completions.create(
                model=config.GROQ_MODEL,
                messages=(
                    [{"role": "system", "content": SYSTEM_PROMPT}]
                    + recent_history
                    + [current_message]
                ),
                max_tokens=512,
                temperature=0.7,
            )
            reply = resp.choices[0].message.content.strip()
            self.conversation.extend([
                current_message,
                {"role": "assistant", "content": reply},
            ])
            self.conversation = self.conversation[
                -(MAX_PREVIOUS_MESSAGES + 2):
            ]
            return reply
        except Exception as e:
            log.error(f"Groq API error: {e}")
            return "Sorry, I am having trouble thinking right now. Please try again."

    # ----------------------------------------------------------
    def _fallback_response(self, text):
        """Simple rule-based fallback when Groq is not available."""
        if "hello" in text or "hi" in text or "ഹലോ" in text:
            return "Hello! I am CareMate. How can I help you today?"
        if "medicine" in text or "tablet" in text or "മരുന്ന്" in text:
            return "It is important to take your medicine on time. Please check with your doctor for dosage."
        if "water" in text or "thirsty" in text or "ദാഹം" in text:
            return "Please drink some water. Staying hydrated is very important!"
        if "pain" in text or "hurt" in text or "വേദന" in text:
            return "I am alerting your caregiver now. Please stay calm."
        if "weather" in text or "rain" in text:
            return "I am not connected to weather services right now. Please check outside!"
        return "I heard you. How can I help you further?"

    # ----------------------------------------------------------
    def _build_status_response(self):
        """Build status response using shared state data."""
        if not self.shared_state:
            return "All systems are functioning normally."
        data = self.shared_state.get_health()
        hr   = data.get("hr", 0)
        temp = data.get("temp", 0.0)
        return (f"System is active. Your heart rate is {hr} beats per minute "
                f"and body temperature is {temp} degrees Celsius.")

    # ----------------------------------------------------------
    def _emergency_call(self):
        """Send emergency alert to caregiver."""
        token   = config.TELEGRAM_BOT_TOKEN
        chat_id = config.TELEGRAM_CHAT_ID
        ts      = time.strftime("%Y-%m-%d %H:%M:%S")

        if token != "YOUR_BOT_TOKEN_HERE":
            msg = f"🆘 EMERGENCY CALL\nTime: {ts}\nElderly person has requested help via voice command."
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            try:
                requests.post(url, json={"chat_id": chat_id, "text": msg}, timeout=8)
                log.info("Emergency call alert sent.")
            except Exception as e:
                log.error(f"Emergency Telegram failed: {e}")

        self.speak("I am alerting your caregiver immediately. Please stay calm. Help is on the way.")

    # ----------------------------------------------------------
    def speak(self, text, lang=None):
        """
        Convert text to speech and play it.
        Auto-detects language based on script.
        """
        if lang is None:
            lang = "ml" if self._is_malayalam(text) else "en"

        log.info(f"CareMate: {text}")

        tmp_path = None
        try:
            tts = gTTS(text=text, lang=lang, slow=False)
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as audio_file:
                tmp_path = audio_file.name
            tts.save(tmp_path)
            self._play_audio(tmp_path)
        except Exception as e:
            log.error("Speech output failed: %s. Falling back to espeak.", e)
            self._espeak(text)
        finally:
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except OSError as e:
                    log.warning("Could not remove temporary speech audio: %s", e)

    # ----------------------------------------------------------
    
    def _play_audio(self, path):
        """Play speech to completion before opening the microphone again."""
        if os.name == "nt":
            import ctypes

            winmm = ctypes.windll.winmm
            alias = "caremate_audio"
            opened = False

            def send_mci_command(command):
                error_code = winmm.mciSendStringW(command, None, 0, 0)
                if error_code:
                    error_message = ctypes.create_unicode_buffer(256)
                    winmm.mciGetErrorStringW(
                        error_code, error_message, len(error_message)
                    )
                    raise OSError(
                        error_message.value or f"MCI error {error_code}"
                    )

            try:
                audio_path = os.path.abspath(path).replace('"', '\\"')
                send_mci_command(
                    f'open "{audio_path}" type mpegvideo alias {alias}'
                )
                opened = True
                send_mci_command(f"play {alias} wait")
            except Exception as e:
                log.error("Windows audio playback failed: %s", e)
                raise RuntimeError(f"Audio playback failed: {e}") from e
            finally:
                if opened:
                    try:
                        send_mci_command(f"close {alias}")
                    except OSError as cleanup_error:
                        log.warning(
                            "Could not close Windows audio playback: %s",
                            cleanup_error,
                        )
        else:
            try:
                if not pygame.mixer.get_init():
                    pygame.mixer.init()

                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(1.0)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
            except Exception as e:
                log.error("Audio playback failed: %s", e)
                raise RuntimeError(f"Audio playback failed: {e}") from e
            finally:
                try:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                except Exception as cleanup_error:
                    log.warning(
                        "Could not release playback audio: %s", cleanup_error
                    )

        # Let the last audio buffer and any room echo fade before listening.
        time.sleep(0.35)

    # ----------------------------------------------------------
    @staticmethod
    def _espeak(text):
        """Fallback TTS using espeak."""
        try:
            subprocess.run(["espeak", "-s", "130", text],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            pass

    # ----------------------------------------------------------
    @staticmethod
    def _is_malayalam(text):
        """Check if text contains Malayalam Unicode characters."""
        for ch in text:
            if '\u0D00' <= ch <= '\u0D7F':
                return True
        return False

    # ----------------------------------------------------------
    def process_text(self, text):
        """External entry point for full_system integration."""
        return self._process(text)

    # ----------------------------------------------------------
    def stop(self):
        self.running = False


# ============================================================
if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.start()
