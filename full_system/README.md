# Full Integrated System

**Run:** `python main.py`
**Dashboard:** http://<raspberry-pi-ip>:5000

Runs all CareMate modules in parallel threads:
- Thread 1: Vision (person following + fall detection on same camera)
- Thread 2: Health monitoring (Arduino sensor data)
- Thread 3: Voice assistant
- Thread 4: Flask dashboard
- Main: Arduino heartbeat + manual command forwarding

**Before running:**
1. Edit ../config.py
2. Flash arduino_main/caremate_arduino.ino to Arduino
3. pip install -r ../requirements.txt --break-system-packages
4. Download YOLO models (see main README)
5. Test motors with module_01/test_motors.py
