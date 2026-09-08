# ============================================================
# CareMate - Central Configuration
# ============================================================

import os
from pathlib import Path

from dotenv import load_dotenv

# Load local environment variables from .env
load_dotenv()

# Project root
BASE_DIR = Path(__file__).resolve().parent


# ============================================================
# Telegram Caregiver Alerts
# ============================================================

TELEGRAM_BOT_TOKEN = os.getenv(
    "CAREMATE_TELEGRAM_BOT_TOKEN",
    "YOUR_BOT_TOKEN_HERE"
)

TELEGRAM_CHAT_ID = os.getenv(
    "CAREMATE_TELEGRAM_CHAT_ID",
    ""
)


# ============================================================
# Arduino / Serial Communication
# ============================================================

SERIAL_PORT = os.getenv(
    "CAREMATE_SERIAL_PORT",
    "COM3"
)

BAUD_RATE = int(os.getenv(
    "CAREMATE_BAUD_RATE",
    "9600"
))

SERIAL_TIMEOUT = 2


# ============================================================
# Camera
# ============================================================

CAMERA_INDEX = int(os.getenv(
    "CAREMATE_CAMERA_INDEX",
    "0"
))

FRAME_WIDTH = 640
FRAME_HEIGHT = 480
SHOW_PREVIEW = False


# ============================================================
# YOLO / Computer Vision
# ============================================================

YOLO_DETECT_MODEL = "yolov8n.pt"
YOLO_POSE_MODEL = "yolov8n-pose.pt"

CONFIDENCE = 0.45

MIN_BOX_WIDTH = 60
MIN_BOX_HEIGHT = 80


# ============================================================
# Person Following
# ============================================================

DEAD_ZONE_RATIO = 0.15
CLOSE_ZONE_RATIO = 0.55
FAR_ZONE_RATIO = 0.18

MOTOR_COMMAND_DELAY = 0.05


# ============================================================
# Fall Detection
# ============================================================

FALL_ASPECT_RATIO = 1.2
FALL_CONFIRM_FRAMES = 4
FALL_COOLDOWN_SEC = 15

FALL_SNAPSHOT_PATH = str(
    BASE_DIR / "data" / "fall_snapshot.jpg"
)


# ============================================================
# Health Monitoring
# ============================================================

HR_LOW = 50
HR_HIGH = 110

TEMP_LOW = 35.0
TEMP_HIGH = 38.5


# ============================================================
# Voice Assistant / LLM
# ============================================================

GROQ_API_KEY = os.getenv(
    "CAREMATE_GROQ_API_KEY",
    "YOUR_GROQ_API_KEY_HERE"
)

# Keep this configurable because model availability can change.
GROQ_MODEL = os.getenv(
    "CAREMATE_GROQ_MODEL",
    "llama3-8b-8192"
)

VOICE_LANGUAGE = os.getenv(
    "CAREMATE_VOICE_LANGUAGE",
    "ml"
)

AUDIO_OUTPUT_FILE = str(
    BASE_DIR / "data" / "caremate_response.mp3"
)


# ============================================================
# Flask Caregiver Dashboard
# ============================================================

FLASK_HOST = os.getenv(
    "CAREMATE_FLASK_HOST",
    "0.0.0.0"
)

FLASK_PORT = int(os.getenv(
    "CAREMATE_FLASK_PORT",
    "5000"
))

SECRET_KEY = os.getenv(
    "CAREMATE_SECRET_KEY",
    "development-only-secret"
)


# ============================================================
# Logging
# ============================================================

LOG_DIR = str(
    BASE_DIR / "logs"
)

LOG_LEVEL = os.getenv(
    "CAREMATE_LOG_LEVEL",
    "INFO"
)