# CareMate — AI-Powered Elderly Care Companion Robot

<p align="center">
  <img src="assets/images/caremate-robot.jpg" alt="CareMate Robot" width="850">
</p>

<p align="center">
  <strong>An AI-assisted mobile robotic platform for elderly safety, monitoring, interaction, and caregiver support.</strong>
</p>

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://www.raspberrypi.com/"><img src="https://img.shields.io/badge/Raspberry%20Pi-5-A22846?style=for-the-badge&logo=raspberrypi&logoColor=white" alt="Raspberry Pi 5"></a>
  <a href="https://www.arduino.cc/"><img src="https://img.shields.io/badge/Arduino-UNO-00979D?style=for-the-badge&logo=arduino&logoColor=white" alt="Arduino UNO"></a>
  <img src="https://img.shields.io/badge/YOLOv8-Computer%20Vision-111827?style=for-the-badge" alt="YOLOv8">
  <img src="https://img.shields.io/badge/OpenCV-Vision-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV">
  <img src="https://img.shields.io/badge/Flask-Dashboard-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Telegram-Alerts-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
</p>

<p align="center">
  <strong>Group 15 Â· MES Kuttippuram Â· Guided by Mr. Abin C Jose</strong>
</p>

---

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [What CareMate Does](#what-caremate-does)
- [System Architecture](#system-architecture)
- [Core Modules](#core-modules)
- [Computer Vision](#computer-vision)
- [Health Monitoring](#health-monitoring)
- [Bilingual Voice Assistant](#bilingual-voice-assistant)
- [Caregiver Dashboard](#caregiver-dashboard)
- [Telegram Alert Workflow](#telegram-alert-workflow)
- [Hardware](#hardware)
- [Hardware Architecture](#hardware-architecture)
- [Pi â†” Arduino Communication](#pi--arduino-communication)
- [Safety Mechanisms](#safety-mechanisms)
- [Technology Stack](#technology-stack)
- [Repository Structure](#repository-structure)
- [Project Gallery](#project-gallery)
- [Demonstrations](#demonstrations)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running CareMate](#running-caremate)
- [Running Individual Modules](#running-individual-modules)
- [Testing](#testing)
- [Observed Performance](#observed-performance)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Team](#team)
- [Disclaimer](#disclaimer)

---

## Overview

**CareMate** is an AI-powered elderly care companion robot that combines **computer vision, robotics, health sensing, voice interaction, web monitoring, and remote caregiver alerts** into a single mobile platform.

The project is designed around a simple principle:

> **A care robot should not only move — it should be able to observe, interpret, interact, assist, and notify a caregiver when human intervention may be required.**

CareMate brings together:

- ðŸ‘ï¸ Vision-based person detection
- ðŸš¶ Person following and movement control
- âš ï¸ Vision-based fall detection
- â¤ï¸ Heart-rate monitoring
- ðŸŒ¡ï¸ Temperature monitoring
- ðŸŽ™ï¸ Malayalam and English voice interaction
- ðŸ–¥ï¸ Web-based caregiver dashboard
- ðŸ“± Telegram notifications with image evidence
- ðŸ¤– Raspberry Pi + Arduino hybrid control
- ðŸ›‘ Hardware-level motor safety through heartbeat monitoring

The system uses a **Raspberry Pi 5** as the high-level computing platform and an **Arduino UNO** for sensor interfacing and motor control.

---

## Problem Statement

Elderly people, particularly those living alone, can face situations where immediate assistance is unavailable.

Common challenges include:

- Falls and accidents
- Delayed caregiver response
- Difficulty continuously monitoring basic health parameters
- Limited mobility of conventional monitoring systems
- Difficulty interacting with technology during emergencies
- Lack of continuous environmental observation

Many existing solutions address only one part of the problem — for example, a wearable health sensor, a fixed camera, or a mobile application.

CareMate explores a more integrated approach by combining **mobility, computer vision, health sensing, voice interaction, and caregiver communication** on one robotic platform.

---

## What CareMate Does

At a high level, CareMate follows this workflow:

```text
                    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                    â”‚       USER           â”‚
                    â”‚  Elderly Individual  â”‚
                    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                               â”‚
              â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
              â”‚                â”‚                â”‚
              â–¼                â–¼                â–¼
           Camera           Sensors           Voice
              â”‚                â”‚                â”‚
              â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                               â–¼
                    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                    â”‚    RASPBERRY PI 5    â”‚
                    â”‚                      â”‚
                    â”‚ Vision + AI          â”‚
                    â”‚ Voice Processing      â”‚
                    â”‚ System Coordination  â”‚
                    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                               â”‚
                         USB / Serial
                               â”‚
                               â–¼
                    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                    â”‚     ARDUINO UNO      â”‚
                    â”‚                      â”‚
                    â”‚ Sensor Interface     â”‚
                    â”‚ Motor Control        â”‚
                    â”‚ Safety Heartbeat     â”‚
                    â””â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”˜
                            â”‚       â”‚
                            â–¼       â–¼
                         Sensors  Motors
                            â”‚
                            â–¼
                    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                    â”‚   CAREGIVER LAYER    â”‚
                    â”‚                      â”‚
                    â”‚ Dashboard + Telegram â”‚
                    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

# System Architecture

CareMate is organized into four functional layers.

### 1. Sensing Layer

Collects information from the physical environment and the user:

- USB camera
- Pulse/heart-rate sensor
- DHT11 temperature sensor
- Microphone

### 2. Intelligence Layer

Runs on the Raspberry Pi:

- YOLOv8 person detection
- YOLOv8 pose estimation
- Fall detection logic
- Person-following logic
- Voice recognition
- LLM-assisted response generation
- System coordination

### 3. Control Layer

The Arduino UNO handles:

- Sensor interfacing
- Motor commands
- L298N motor-driver control
- Serial communication
- Hardware heartbeat safety stop

### 4. Caregiver Layer

Provides remote visibility and alerts:

- Flask dashboard
- Live camera stream
- Health readings
- Fall status
- Robot controls
- Activity log
- Telegram notifications
- Caregiver emergency confirmation

---

## System Architecture Diagram

<p align="center">
  <img src="assets/images/system-architecture.jpg" alt="CareMate System Architecture" width="900">
</p>

---

# Core Modules

| Module | Purpose | Main Technology |
|---|---|---|
| `module_01_person_following` | Detect and follow the target person | YOLOv8n + OpenCV |
| `module_02_fall_detection` | Detect potential falls from body posture | YOLOv8n-pose |
| `module_03_health_monitoring` | Read and monitor heart rate and temperature | Arduino + Python |
| `module_04_voice_assistant` | Malayalam/English voice interaction | SpeechRecognition + Groq + gTTS |
| `module_05_dashboard_alerts` | Monitoring dashboard and notifications | Flask + Telegram |
| `full_system` | Integrate all modules | Python + threading |
| `arduino_main` | Motor, sensor, and safety control | Arduino C/C++ |

---

# Computer Vision

Computer vision is one of the primary intelligence components of CareMate.

The camera feed is processed on the Raspberry Pi for:

- Person detection
- Person localization
- Person following
- Pose estimation
- Fall detection
- Visual monitoring

The project uses lightweight YOLOv8 models intended for edge deployment.

---

## Person Detection & Following

The person-following module uses **YOLOv8n** to detect people in the camera frame.

The implementation:

1. Captures a camera frame.
2. Detects objects belonging to the `person` class.
3. Selects the largest detected person bounding box as the target.
4. Filters very small detections.
5. Calculates the person's position relative to the frame center.
6. Determines a movement command.
7. Sends the command to the Arduino through serial communication.

```text
Camera Frame
     â”‚
     â–¼
YOLOv8n Person Detection
     â”‚
     â–¼
Target Bounding Box
     â”‚
     â–¼
Position / Distance Estimation
     â”‚
     â–¼
Movement Decision
     â”‚
 â”Œâ”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
 â–¼   â–¼               â–¼
LEFT FORWARD       RIGHT
     â”‚
     â–¼
   STOP
     â”‚
     â–¼
Arduino â†’ L298N â†’ Motors
```

### Movement Commands

| Command | Meaning |
|---|---|
| `F` | Forward |
| `B` | Backward |
| `L` | Left |
| `R` | Right |
| `S` | Stop |

<p align="center">
  <img src="assets/images/person-following.jpg" alt="CareMate Person Following" width="850">
</p>

---

# Fall Detection

Fall detection is a core safety feature of CareMate.

The system uses **YOLOv8n-pose** to obtain human pose information and combines it with geometric posture analysis.

### Detection logic

The implementation evaluates:

- Person bounding-box aspect ratio
- Head-to-hip relative position
- Minimum detection dimensions
- Consecutive frames satisfying fall conditions
- Alert cooldown

A potential fall is not immediately treated as a confirmed emergency.

```text
Camera Frame
     â”‚
     â–¼
YOLOv8n-Pose
     â”‚
     â–¼
Person + Pose Keypoints
     â”‚
     â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
     â–¼               â–¼
Bounding Box     Keypoint Analysis
Aspect Ratio     Head / Hip Position
     â”‚               â”‚
     â””â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜
             â–¼
       Fall Candidate
             â”‚
             â–¼
   Consecutive Frame Check
             â”‚
             â–¼
      FALL CONFIRMED
             â”‚
      â”Œâ”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”
      â–¼             â–¼
   Snapshot      Telegram Alert
```

The implementation currently confirms a fall after the configured number of consecutive frames and applies an alert cooldown to avoid repeated notifications.

<p align="center">
  <img src="assets/images/fall-detection.jpg" alt="CareMate Fall Detection" width="850">
</p>

---

## Fall Alert Evidence

When a fall is confirmed, CareMate captures a snapshot and can send it to the caregiver through Telegram.

<p align="center">
  <img src="assets/images/fall-detection-alert.jpg" alt="CareMate Fall Detection Alert" width="850">
</p>

---

# Health Monitoring

CareMate uses the Arduino UNO to interface with basic physiological/environmental sensors.

### Heart Rate

A pulse sensor provides heart-rate readings to the Arduino.

### Temperature

A DHT11 sensor provides temperature readings.

The Arduino periodically transmits the readings to the Raspberry Pi as JSON:

```json
{
  "hr": 72,
  "temp": 36.5,
  "hum": 60.0,
  "status": "ok"
}
```

The Python health-monitoring module:

- Reads the serial stream
- Parses sensor data
- Maintains the latest readings
- Logs readings to CSV
- Checks configured thresholds
- Generates health alerts when required
- Makes readings available to the dashboard

---

# Bilingual Voice Assistant

CareMate includes a voice assistant designed for **English and Malayalam** interaction.

### Voice pipeline

```text
Microphone
    â”‚
    â–¼
Speech Recognition
    â”‚
    â–¼
English / Malayalam Text
    â”‚
    â–¼
Command / LLM Processing
    â”‚
    â–¼
Response Text
    â”‚
    â–¼
gTTS
    â”‚
    â–¼
Audio Playback
```

The assistant supports local commands such as:

- Status
- Stop
- Help
- Call caregiver
- Emergency

Other conversational queries can be processed using the configured Groq LLM integration.

<p align="center">
  <img src="assets/images/voice-assistant.jpg" alt="CareMate Voice Assistant" width="850">
</p>

> Voice responses are intended as an assistive interaction layer and should not be treated as professional medical advice.

---

# Caregiver Dashboard

CareMate provides a Flask-based web dashboard for centralized monitoring.

The dashboard includes:

- â¤ï¸ Heart-rate information
- ðŸŒ¡ï¸ Temperature information
- ðŸš¨ Fall status
- ðŸ“¹ Live camera feed
- ðŸ¤– Manual robot controls
- ðŸš¶ Person-following control
- ðŸ“‹ Activity log
- ðŸ“¡ System status
- ðŸ”” Alert information

The dashboard is accessible over the local network:

```text
http://<raspberry-pi-ip>:5000
```

<p align="center">
  <img src="assets/images/dashboard.jpg" alt="CareMate Caregiver Dashboard" width="950">
</p>

---

# Telegram Alert Workflow

Telegram is used as the remote caregiver notification layer.

A confirmed fall can trigger:

1. Snapshot capture
2. Telegram photo notification
3. Event timestamp
4. Caregiver confirmation buttons

```text
Potential Fall
      â”‚
      â–¼
Fall Confirmation Logic
      â”‚
      â–¼
Snapshot Captured
      â”‚
      â–¼
Telegram Photo Alert
      â”‚
      â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚   CAREGIVER RECEIVES  â”‚
â”‚       ALERT           â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
            â”‚
       â”Œâ”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”
       â–¼          â–¼
   CONFIRM      FALSE ALARM
       â”‚          â”‚
       â–¼          â–¼
Emergency      Dismiss
Response       Alert
```

<p align="center">
  <img src="assets/images/telegram-alert.jpg" alt="CareMate Telegram Alert" width="700">
</p>

<p align="center">
  <img src="assets/images/telegram-notification.jpg" alt="CareMate Telegram Notification" width="700">
</p>

---

# Human-in-the-Loop Safety

CareMate is designed so that AI detection assists rather than blindly replaces human judgment.

```text
AI Detection
     â”‚
     â–¼
Potential Fall
     â”‚
     â–¼
Caregiver Notification
     â”‚
     â–¼
Human Confirmation
     â”‚
 â”Œâ”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
 â–¼               â–¼
Emergency      False Alarm
Response       / Dismiss
```

This design is particularly important because vision-based systems can experience false positives and false negatives under changing environmental conditions.

---

# Hardware

The physical CareMate prototype uses a mobile four-wheel robotic platform.

### Main components

| Component | Role |
|---|---|
| Raspberry Pi 5 | High-level processing and AI |
| Arduino UNO | Sensor and motor interfacing |
| L298N Motor Driver | DC motor control |
| USB Webcam | Vision input |
| 4 Ã— DC Geared Motors | Robot movement |
| DHT11 | Temperature sensing |
| Pulse Sensor | Heart-rate sensing |
| 12V Battery | Motor power |
| 5V Buck Converter | Regulated low-voltage power |
| Speaker / Audio Output | Voice responses |

<p align="center">
  <img src="assets/images/caremate-robot.jpg" alt="CareMate Physical Prototype" width="900">
</p>

---

# Hardware Architecture

The robot follows a split architecture:

- **Raspberry Pi:** high-level AI, vision, voice, communication, and system coordination
- **Arduino:** low-level sensors, motor control, and hardware safety
- **L298N:** motor-driver interface
- **12V battery:** primary motor power
- **5V buck converter:** regulated logic power

<p align="center">
  <img src="assets/images/hardware-architecture.jpg" alt="CareMate Hardware Architecture" width="900">
</p>

### Simplified architecture

```text
                    USB CAMERA
                        â”‚
                        â–¼
                 â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                 â”‚ Raspberry Piâ”‚
                 â”‚      5      â”‚
                 â””â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”˜
                        â”‚
                   USB / Serial
                        â”‚
                        â–¼
                 â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                 â”‚ Arduino UNO â”‚
                 â””â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”˜
                        â”‚
              â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
              â–¼                   â–¼
        Health Sensors       L298N Driver
              â”‚                   â”‚
              â”‚             â”Œâ”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”
              â”‚             â–¼           â–¼
              â”‚         Left Motors  Right Motors
              â”‚
              â””â”€â”€â”€â”€â”€â”€â–º Sensor Data
```

---

# Hardware Wiring

## L298N â†’ Arduino UNO

| L298N | Arduino | Purpose |
|---|---|---|
| ENA | D6 (PWM) | Left motor speed |
| IN1 | D7 | Left motor direction |
| IN2 | D8 | Left motor direction |
| ENB | D5 (PWM) | Right motor speed |
| IN3 | D9 | Right motor direction |
| IN4 | D10 | Right motor direction |

## DHT11 â†’ Arduino UNO

| DHT11 | Arduino |
|---|---|
| VCC | 5V |
| GND | GND |
| DATA | D2 |

## Pulse Sensor â†’ Arduino UNO

| Pulse Sensor | Arduino |
|---|---|
| VCC | 5V |
| GND | GND |
| Signal | A0 |

## Raspberry Pi â†’ Arduino

The Raspberry Pi communicates with the Arduino through USB serial.

Default configuration:

```text
/dev/ttyACM0
9600 baud
```

---

# Pi â†” Arduino Communication

CareMate uses a simple serial protocol between the Raspberry Pi and Arduino.

## Raspberry Pi â†’ Arduino

| Data | Meaning |
|---|---|
| `F` | Move forward |
| `B` | Move backward |
| `L` | Turn left |
| `R` | Turn right |
| `S` | Stop |
| `K` | Heartbeat acknowledgement |

## Arduino â†’ Raspberry Pi

| Data | Meaning |
|---|---|
| `H` | Heartbeat, approximately every 1 second |
| JSON sensor packet | Health data, approximately every 2 seconds |

Example:

```json
{"hr":72,"temp":36.5,"hum":60.0,"status":"ok"}
```

---

# Safety Mechanisms

### Arduino Heartbeat Safety Stop

The Arduino expects periodic heartbeat acknowledgements from the Raspberry Pi.

```text
Raspberry Pi
     â”‚
     â”‚ K
     â”‚
     â–¼
Arduino
     â”‚
     â”‚ heartbeat timeout
     â–¼
No acknowledgement for 3 seconds
     â”‚
     â–¼
STOP ALL MOTORS
```

If the Arduino does not receive the expected `K` heartbeat within the configured timeout, it automatically stops the motors.

This provides a hardware-level fail-safe against loss of Raspberry Pi communication.

### Other safety/robustness mechanisms

- Fall confirmation over multiple frames
- Fall-alert cooldown
- Health-alert cooldown
- Minimum person bounding-box size
- Motor diagnostic test before person following
- Manual stop control
- Caregiver confirmation for fall alerts

---

# Technology Stack

## Hardware

- Raspberry Pi 5
- Arduino UNO
- L298N motor driver
- USB webcam
- DC geared motors
- DHT11
- Pulse sensor
- 12V battery
- 5V buck converter
- Robotic chassis
- Speaker/audio output

## Software & AI

- Python
- OpenCV
- Ultralytics YOLOv8
- YOLOv8n
- YOLOv8n-pose
- NumPy
- Flask
- PySerial
- SpeechRecognition
- gTTS
- Pygame
- Groq API
- Telegram Bot API
- Arduino C/C++

---

# Repository Structure

```text
CAREMATE/
â”‚
â”œâ”€â”€ README.md
â”œâ”€â”€ .gitignore
â”œâ”€â”€ .env.example
â”œâ”€â”€ config.py
â”œâ”€â”€ requirements.txt
â”‚
â”œâ”€â”€ arduino_main/
â”‚   â””â”€â”€ caremate_arduino.ino
â”‚
â”œâ”€â”€ assets/
â”‚   â”œâ”€â”€ dashboard/
â”‚   â”œâ”€â”€ demo/
â”‚   â”‚   â”œâ”€â”€ caremate-demo.mp4
â”‚   â”‚   â””â”€â”€ fall-detection-demo.mp4
â”‚   â”œâ”€â”€ hardware/
â”‚   â”œâ”€â”€ hero/
â”‚   â”œâ”€â”€ images/
â”‚   â”‚   â”œâ”€â”€ caremate-robot.jpg
â”‚   â”‚   â”œâ”€â”€ dashboard.jpg
â”‚   â”‚   â”œâ”€â”€ fall-detection-alert.jpg
â”‚   â”‚   â”œâ”€â”€ fall-detection.jpg
â”‚   â”‚   â”œâ”€â”€ hardware-architecture.jpg
â”‚   â”‚   â”œâ”€â”€ person-following.jpg
â”‚   â”‚   â”œâ”€â”€ system-architecture.jpg
â”‚   â”‚   â”œâ”€â”€ telegram-alert.jpg
â”‚   â”‚   â”œâ”€â”€ telegram-notification.jpg
â”‚   â”‚   â””â”€â”€ voice-assistant.jpg
â”‚   â””â”€â”€ vision/
â”‚
â”œâ”€â”€ docs/
â”‚
â”œâ”€â”€ full_system/
â”‚   â”œâ”€â”€ main.py
â”‚   â”œâ”€â”€ shared_state.py
â”‚   â””â”€â”€ README.md
â”‚
â”œâ”€â”€ models/
â”‚
â”œâ”€â”€ module_01_person_following/
â”‚   â”œâ”€â”€ person_following.py
â”‚   â”œâ”€â”€ test_motors.py
â”‚   â””â”€â”€ README.md
â”‚
â”œâ”€â”€ module_02_fall_detection/
â”‚   â”œâ”€â”€ fall_detection.py
â”‚   â””â”€â”€ README.md
â”‚
â”œâ”€â”€ module_03_health_monitoring/
â”‚   â”œâ”€â”€ health_monitor.py
â”‚   â”œâ”€â”€ arduino_health/
â”‚   â”‚   â””â”€â”€ arduino_health.ino
â”‚   â””â”€â”€ README.md
â”‚
â”œâ”€â”€ module_04_voice_assistant/
â”‚   â”œâ”€â”€ voice_assistant.py
â”‚   â””â”€â”€ README.md
â”‚
â””â”€â”€ module_05_dashboard_alerts/
    â”œâ”€â”€ app.py
    â”œâ”€â”€ telegram_bot.py
    â”œâ”€â”€ templates/
    â”‚   â””â”€â”€ index.html
    â””â”€â”€ README.md
```

---

# Project Gallery

## Physical Prototype

<p align="center">
  <img src="assets/images/caremate-robot.jpg" alt="CareMate Robot" width="850">
</p>

## Hardware Architecture

<p align="center">
  <img src="assets/images/hardware-architecture.jpg" alt="Hardware Architecture" width="850">
</p>

## System Architecture

<p align="center">
  <img src="assets/images/system-architecture.jpg" alt="System Architecture" width="850">
</p>

## Fall Detection

<p align="center">
  <img src="assets/images/fall-detection.jpg" alt="Fall Detection" width="850">
</p>

## Person Following

<p align="center">
  <img src="assets/images/person-following.jpg" alt="Person Following" width="850">
</p>

## Voice Assistant

<p align="center">
  <img src="assets/images/voice-assistant.jpg" alt="Voice Assistant" width="850">
</p>

## Dashboard

<p align="center">
  <img src="assets/images/dashboard.jpg" alt="Caregiver Dashboard" width="950">
</p>

---

# Demonstrations

## CareMate Robot Demonstration

[â–¶ Open CareMate Demo](assets/demo/caremate-demo.mp4)

## Fall Detection Demonstration

[â–¶ Open Fall Detection Demo](assets/demo/fall-detection-demo.mp4)

> GitHub's handling of large MP4 files can vary. The repository keeps the original demonstration files under `assets/demo/`; if GitHub does not render an inline preview, open the file using the links above.

---

# Installation

CareMate is primarily designed for deployment on a **Raspberry Pi running Linux**, with an Arduino UNO connected through USB.

## 1. Clone the Repository

```bash
git clone https://github.com/Abhishek-palakkeel/CAREMATE.git
cd CAREMATE
```

## 2. Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

## 3. Install Python Dependencies

On the Raspberry Pi:

```bash
pip install -r requirements.txt --break-system-packages
```

If your environment does not require `--break-system-packages`, the standard command is:

```bash
pip install -r requirements.txt
```

## 4. Install Required System Packages

```bash
sudo apt update
sudo apt install espeak portaudio19-dev mpg321
```

## 5. Install the Arduino Library

Open the Arduino IDE and install:

**DHT sensor library by Adafruit**

Then:

1. Open `arduino_main/caremate_arduino.ino`
2. Select **Arduino UNO**
3. Select the correct serial port
4. Upload the sketch

---

# Configuration

Before running CareMate, configure the central `config.py` file.

Important configuration values include:

```python
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
TELEGRAM_CHAT_ID   = "YOUR_CHAT_ID"

SERIAL_PORT        = "/dev/ttyACM0"
BAUD_RATE          = 9600

CAMERA_INDEX       = 0

GROQ_API_KEY       = "YOUR_GROQ_API_KEY_HERE"
```

### Important

**Never commit real API keys, Telegram bot tokens, passwords, or other credentials to GitHub.**

Use placeholder values in the public repository and keep private credentials out of version control.

---

# Download YOLO Models

The project uses two lightweight YOLOv8 models:

- `yolov8n.pt` — person detection
- `yolov8n-pose.pt` — pose estimation / fall detection

Download them with:

```bash
python3 -c "
from ultralytics import YOLO
YOLO('yolov8n.pt')
YOLO('yolov8n-pose.pt')
print('Models downloaded.')
"
```

The models may also be downloaded automatically by Ultralytics when loaded if they are not already present.

---

# Running CareMate

## Recommended startup sequence

### 1. Connect Arduino

Connect the Arduino UNO to the Raspberry Pi through USB.

### 2. Test the motors

**Do this before running person following.**

```bash
cd module_01_person_following
python test_motors.py
```

The diagnostic checks:

```text
FORWARD
STOP
BACKWARD
STOP
LEFT
STOP
RIGHT
STOP
```

If a motor rotates in the wrong direction, inspect the corresponding motor wiring.

### 3. Start the complete system

```bash
cd full_system
python main.py
```

The integrated system launches:

```text
Vision Thread
Health Monitoring Thread
Voice Assistant Thread
Flask Dashboard Thread
Arduino Serial / Heartbeat Management
```

### 4. Open the dashboard

From another device on the same network:

```text
http://<raspberry-pi-ip>:5000
```

---

# Running Individual Modules

Each subsystem can also be tested independently.

| Module | Command |
|---|---|
| Person Following | `cd module_01_person_following && python person_following.py` |
| Motor Test | `cd module_01_person_following && python test_motors.py` |
| Fall Detection | `cd module_02_fall_detection && python fall_detection.py` |
| Health Monitoring | `cd module_03_health_monitoring && python health_monitor.py` |
| Voice Assistant | `cd module_04_voice_assistant && python voice_assistant.py` |
| Dashboard | `cd module_05_dashboard_alerts && python app.py` |
| Telegram Test | `cd module_05_dashboard_alerts && python telegram_bot.py` |

---

# Testing

CareMate was tested across the major functional areas.

### Computer Vision

- Person detection
- Pose/keypoint detection
- Fall detection
- Person tracking
- Direction estimation

### Robotics

- Forward movement
- Backward movement
- Left movement
- Right movement
- Stop command
- Person-following behaviour

### Health Monitoring

- Heart-rate input
- Temperature input
- Serial JSON parsing
- Threshold-based alerts
- Health data logging

### Voice

- Voice input
- English recognition
- Malayalam recognition
- Command recognition
- System responses
- Stop command
- Caregiver/emergency command

### Communication

- Telegram text alert
- Telegram photo alert
- Caregiver confirmation
- False-alarm handling

### Dashboard

- Live camera stream
- Health information
- Fall status
- Robot controls
- Activity logs
- System status

---

# Observed Performance

Testing and project review observations showed:

- Real-time fall detection using pose estimation
- Reliable person detection and tracking under suitable lighting conditions
- Telegram alert delivery in approximately 1â€“2 seconds during testing
- Voice assistant responses in approximately 1â€“2 seconds during testing
- Raspberry Pi edge processing suitable for the implemented lightweight models

Performance is environment-dependent and should not be interpreted as a medical or production-grade benchmark.

---

# Limitations

CareMate is an **academic and engineering prototype**, and several limitations remain.

### Computer Vision

- Performance depends on lighting conditions.
- Full occlusion can cause tracking loss.
- Fast movement can reduce tracking stability.
- Vision-based fall detection can produce false positives or false negatives.

### Voice

- Recognition accuracy can decrease with background noise.
- Malayalam recognition depends on speech clarity and acoustic conditions.
- Internet/API availability can affect LLM-assisted responses.

### Hardware

- Motor behaviour depends on surface conditions, battery state, and mechanical alignment.
- Sensor readings depend on placement, calibration, and sensor quality.
- The prototype does not yet provide production-grade autonomous navigation.

### Connectivity

- Telegram notifications require network connectivity.
- The caregiver dashboard is intended for the local network deployment used by the prototype.

### Medical Use

CareMate is **not a certified medical device** and should not be used as a replacement for professional medical equipment, emergency services, or human supervision.

---

# Future Improvements

## Robotics

- Autonomous navigation
- Obstacle avoidance
- Wheel encoders
- LiDAR/depth sensing
- Mapping and localization
- Better path planning
- Automatic return-to-user behaviour

## Computer Vision & AI

- Temporal fall-detection models
- Improved false-positive reduction
- Multi-person tracking
- Activity recognition
- Behaviour anomaly detection
- Personalized monitoring

## Health Monitoring

- Additional physiological sensors
- Improved sensor calibration
- Historical health trends
- Long-term data visualization
- More robust alert classification

## Voice Assistant

- Stronger offline speech recognition
- Improved Malayalam support
- Context-aware conversations
- Personalized interaction
- More robust noisy-environment recognition

## Caregiver Platform

- Historical dashboards
- Mobile application
- Multiple caregiver accounts
- Alert severity levels
- Emergency escalation
- Cloud synchronization where appropriate

---

# Design Philosophy

CareMate is not intended to be just a mobile robot.

The broader design goal is to combine:

```text
        â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
        â”‚    SAFETY    â”‚
        â””â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜
               â”‚
        â”Œâ”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”
        â”‚   CAREMATE   â”‚
        â””â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜
               â”‚
      â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”
      â”‚        â”‚        â”‚
      â–¼        â–¼        â–¼
   HEALTH  ASSISTANCE  AI
      â”‚        â”‚        â”‚
      â””â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”˜
               â”‚
               â–¼
          CAREGIVER
```

The project explores how **AI perception, embedded systems, robotics, natural interaction, and remote communication** can work together to create a more proactive elderly-care platform.

---

# Team

| Member | Responsibility |
|---|---|
| **Abhishekh P** | Vision & System Lead |
| **Ranila CP** | Voice Assistant Developer |
| **Reeha Al Samar** | Dashboard & UI Developer |
| **Hiba Shamsudheen** | IoT & Documentation Lead |

**Institution:** MES Kuttippuram  
**Project:** Group 15  
**Guide:** Mr. Abin C Jose

---

# Disclaimer

CareMate is an academic/engineering prototype developed for research, learning, demonstration, and evaluation purposes.

It is **not a certified medical device, emergency response system, or substitute for professional healthcare**.

Fall detections, health readings, voice responses, and caregiver alerts may be affected by environmental conditions, sensor limitations, network availability, and model accuracy. Critical situations must always be independently verified by a responsible human or appropriate emergency/medical service.

---

## Acknowledgements

The project makes use of open-source software, machine-learning frameworks, embedded platforms, and hardware technologies including Python, OpenCV, Ultralytics YOLO, Flask, Arduino, Raspberry Pi, and related libraries and services.

---

<p align="center">
  <strong>CAREMATE</strong><br>
  AI Â· Robotics Â· Computer Vision Â· Embedded Systems Â· Elderly Care
</p>

