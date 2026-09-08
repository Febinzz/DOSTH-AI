# Module 01 – Person Detection & Following

**Run:** `python person_following.py`
**Test motors first:** `python test_motors.py`

Detects the nearest person using YOLOv8n and sends motor commands (F/L/R/S) to Arduino to keep the person centered in frame.

Key settings in config.py:
- `CONFIDENCE = 0.45` — detection threshold
- `MIN_BOX_WIDTH/HEIGHT = 60/80` — ignore small detections (chair legs)
- `DEAD_ZONE_RATIO = 0.15` — tolerance before turning
