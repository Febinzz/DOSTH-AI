# Module 03 – Health Monitoring

**Run:** `python health_monitor.py`
**Arduino sketch:** `arduino_health/arduino_health.ino`

Reads heart rate (BPM) and temperature (°C) from Arduino over serial.
Arduino sends JSON every 2 seconds: `{"hr":72,"temp":36.5,"hum":60.0,"status":"ok"}`

Sends Telegram + espeak alerts if readings are abnormal.
Logs all readings to CSV file at config.LOG_DIR.
