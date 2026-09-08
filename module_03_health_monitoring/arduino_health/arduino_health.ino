// ============================================================
//   CareMate - Arduino Health Sensor Sketch (Standalone Test)
//   For testing health sensors independently of motor control.
//
//   Sensors:
//     - DHT11 Temperature & Humidity sensor → Pin D2
//     - Pulse Sensor (analog)               → Pin A0
//
//   Output (Serial, every 2 seconds):
//     {"hr":72,"temp":36.5,"hum":60.0,"status":"ok"}
//
//   Install DHT library:
//     Arduino IDE → Sketch → Include Library → Manage Libraries
//     Search "DHT sensor library" by Adafruit → Install
// ============================================================

#include <DHT.h>

#define DHT_PIN   2
#define DHT_TYPE  DHT11
#define PULSE_PIN A0

DHT dht(DHT_PIN, DHT_TYPE);

// BPM tracking
int   bpmBuffer[10];
int   bpmIndex      = 0;
int   currentBPM    = 0;
bool  beatDetected  = false;
unsigned long lastBeatMs = 0;
const int threshold  = 550;   // Adjust for your pulse sensor sensitivity

// Timing
unsigned long lastSendMs = 0;
const unsigned long SEND_INTERVAL = 2000;

// ============================================================
void setup() {
  Serial.begin(9600);
  dht.begin();
  for (int i = 0; i < 10; i++) bpmBuffer[i] = 70;  // Init BPM buffer
  Serial.println("{\"status\":\"Health sensor ready\"}");
}

// ============================================================
void loop() {
  readPulse();

  if (millis() - lastSendMs >= SEND_INTERVAL) {
    sendData();
    lastSendMs = millis();
  }
}

// ============================================================
void readPulse() {
  int val = analogRead(PULSE_PIN);
  unsigned long now = millis();

  if (val > threshold && !beatDetected) {
    beatDetected = true;
    if (lastBeatMs > 0) {
      unsigned long interval = now - lastBeatMs;
      if (interval > 300 && interval < 2000) {
        int bpm = 60000 / interval;
        bpmBuffer[bpmIndex % 10] = bpm;
        bpmIndex++;
        int sum = 0;
        for (int i = 0; i < 10; i++) sum += bpmBuffer[i];
        currentBPM = sum / 10;
      }
    }
    lastBeatMs = now;
  }
  if (val < threshold - 50) beatDetected = false;
}

// ============================================================
void sendData() {
  float temp = dht.readTemperature();
  float hum  = dht.readHumidity();
  if (isnan(temp)) temp = 0.0;
  if (isnan(hum))  hum  = 0.0;

  Serial.print("{\"hr\":");
  Serial.print(currentBPM);
  Serial.print(",\"temp\":");
  Serial.print(temp, 1);
  Serial.print(",\"hum\":");
  Serial.print(hum, 1);
  Serial.println(",\"status\":\"ok\"}");
}
