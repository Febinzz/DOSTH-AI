# Module 02 – Fall Detection

**Run:** `python fall_detection.py`

Detects falls using YOLOv8n-pose by checking:
1. Bounding box aspect ratio (wide box = horizontal = fallen)
2. Keypoint positions (head at or below hip level)

On confirmed fall: saves snapshot → sends Telegram photo alert → espeak voice alert.

Key settings in config.py:
- `FALL_ASPECT_RATIO = 1.2` — w/h ratio threshold
- `FALL_CONFIRM_FRAMES = 4` — frames before triggering alert
- `FALL_COOLDOWN_SEC = 15` — minimum seconds between alerts
