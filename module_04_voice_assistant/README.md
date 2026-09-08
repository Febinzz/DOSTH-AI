# Module 04 – Voice Assistant

**Run:** `python voice_assistant.py`
**Requires:** `sudo apt install espeak portaudio19-dev mpg321`
**Requires:** Groq API key (free at console.groq.com) in config.py

Listens via microphone, recognizes speech in Malayalam (ml-IN) or English (en-IN),
sends to Groq LLM for intelligent response, speaks reply via gTTS.

Special commands: "status", "stop", "help", "call caregiver", "emergency"
