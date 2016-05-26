#include <NewPing.h>

#define TRIGGER_PIN  2  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     3  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 200 // Maximum distance (in cm) to ping.

// Declare L298N Dual H-Bridge Motor Controller directly since there is not a library to load.
const int speed = 200;
// Back Motor 1 (Left)
uint8_t int1B1 = 4;
uint8_t int2B1 = 7;
int enB1 = 5; // Needs to be a PWM pin to be able to control motor speed
// Back Motor 2 (Right)
uint8_t int1B2 = 8;
uint8_t int2B2 = 9;
int enB2 = 6; // Needs to be a PWM pin to be able to control motor speed
// Front Motor 1 (Left)
uint8_t int1F1 = 12;
uint8_t int2F1 = 13;
int enF1 = 10; // Needs to be a PWM pin to be able to control motor speed
// Front Motor 2 (Right)
uint8_t int1F2 = A0;
uint8_t int2F2 = A1;
int enF2 = 11; // Needs to be a PWM pin to be able to control motor speed

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.

void setup() {
  
  pinMode(int1B1,OUTPUT);
  pinMode(int2B1,OUTPUT);
  pinMode(int1B2,OUTPUT);
  pinMode(int2B2,OUTPUT);
  pinMode(int1F1,OUTPUT);
  pinMode(int2F1,OUTPUT);
  pinMode(int1F2,OUTPUT);
  pinMode(int2F2,OUTPUT);
  pinMode(enB1,OUTPUT);
  pinMode(enB2,OUTPUT);
  pinMode(enF1,OUTPUT);
  pinMode(enF2,OUTPUT);

  // Open serial communication @ 115200 baud and wait for port to open:
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
}

void loop() {
  // Wait 50ms between pings (about 20 pings/sec). 29ms should be the shortest delay between pings.
  // delay(50); 
  int cm = sonar.ping_cm();
  if (cm <= 15) {
    stopMotor();
  }
  doStaff(cm); // All logic controller is implemented here
}

void doStaff(int cm) {
  uint8_t serIn = 0;
  if (Serial.available()) {
    serIn = Serial.read();
  }
  
  switch (serIn) {
    case 1:
      if (cm <= 15) {
        stopMotor();
        delay(50);
      } else {
        // move robot forward
        goForward();
      }
      break;
    case 2:
      // move robot backward
      goBackward();
      break;
    case 3:
      // move robot to left direction
      goLeft();
      break;
    case 4:
      // move robot to right direction
      goRight();
      break;
    default:
      // default state
      stopMotor();
      break;
  }
}

void stopMotor() {
  analogWrite(enB1, 0);
  analogWrite(enB2, 0);
  analogWrite(enF1, 0);
  analogWrite(enF2, 0);
}

void goForward() {
  // Stop motor before change direction
  stopMotor();
  delay(100);
  
  // Back Motor
  digitalWrite(int1B1, HIGH);
  digitalWrite(int2B1, LOW);
  digitalWrite(int1B2, HIGH);
  digitalWrite(int2B2, LOW);
  analogWrite(enB1, speed);
  analogWrite(enB2, speed);
  // Front Motor
  digitalWrite(int1F1, HIGH);
  digitalWrite(int2F1, LOW);
  digitalWrite(int1F2, HIGH);
  digitalWrite(int2F2, LOW);
  analogWrite(enF1, speed);
  analogWrite(enF2, speed);
}

void goBackward() {
  // Stop motor before change direction
  stopMotor();
  delay(100);
  
  // Back Motor
  digitalWrite(int1B1, LOW);
  digitalWrite(int2B1, HIGH);
  digitalWrite(int1B2, LOW);
  digitalWrite(int2B2, HIGH);
  analogWrite(enB1, speed);
  analogWrite(enB2, speed);
  // Front Motor
  digitalWrite(int1F1, LOW);
  digitalWrite(int2F1, HIGH);
  digitalWrite(int1F2, LOW);
  digitalWrite(int2F2, HIGH);
  analogWrite(enF1, speed);
  analogWrite(enF2, speed);
}

void goLeft() {
  // Stop motor before change direction
  stopMotor();
  delay(100);
  
  // Back Motor
  digitalWrite(int1B1, LOW);
  digitalWrite(int2B1, HIGH);
  digitalWrite(int1B2, HIGH);
  digitalWrite(int2B2, LOW);
  analogWrite(enB1, speed);
  analogWrite(enB2, speed);
  // Front Motor
  digitalWrite(int1F1, LOW);
  digitalWrite(int2F1, HIGH);
  digitalWrite(int1F2, HIGH);
  digitalWrite(int2F2, LOW);
  analogWrite(enF1, speed);
  analogWrite(enF2, speed);
}

void goRight() {
  // Stop motor before change direction
  stopMotor();
  delay(100);
  
  // Back Motor
  digitalWrite(int1B1, HIGH);
  digitalWrite(int2B1, LOW);
  digitalWrite(int1B2, LOW);
  digitalWrite(int2B2, HIGH);
  analogWrite(enB1, speed);
  analogWrite(enB2, speed);
  // Front Motor
  digitalWrite(int1F1, HIGH);
  digitalWrite(int2F1, LOW);
  digitalWrite(int1F2, LOW);
  digitalWrite(int2F2, HIGH);
  analogWrite(enF1, speed);
  analogWrite(enF2, speed);
}

