#include <NewPing.h>

#define TRIGGER_PIN  2  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     3  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 200 // Maximum distance (in cm) to ping.

// Declare L298N Dual H-Bridge Motor Controller directly
// since there is not a library to load.
// 1 => left; 2 => right
// Back Motor 1 (Left)
#define int1B1 4
#define int2B1 5
// Back Motor 2 (Right)
#define int1B2 8
#define int2B2 9
// Front Motor 1 (Left)
#define int1F1 6
#define int2F1 7
// Front Motor 2 (Right)
#define int1F2 10
#define int2F2 11

const int DELAY = 500;

unsigned long cm = 0;
// NewPing setup of pins and maximum distance.
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); 

void setup() {
  // declear pin
  pinMode(int1B1,OUTPUT);
  pinMode(int2B1,OUTPUT);
  pinMode(int1B2,OUTPUT);
  pinMode(int2B2,OUTPUT);
  pinMode(int1F1,OUTPUT);
  pinMode(int2F1,OUTPUT);
  pinMode(int1F2,OUTPUT);
  pinMode(int2F2,OUTPUT);

  // set initial pin state
  digitalWrite(int1B1,LOW);
  digitalWrite(int2B1,LOW);
  digitalWrite(int1B2,LOW);
  digitalWrite(int2B2,LOW);
  digitalWrite(int1F1,LOW);
  digitalWrite(int2F1,LOW);
  digitalWrite(int1F2,LOW);
  digitalWrite(int2F2,LOW);

  // Open serial communication @ 115200 baud and wait for port to open:
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
}

void loop() {
  // Wait 50ms between pings (about 20 pings/sec). 
  // 29ms should be the shortest delay between pings.
  delay(50); 
  cm = sonar.ping_cm();
  Serial.print("Ping: ");
  // Send ping, get distance in cm and print result (0 = outside set distance range)
  Serial.print(cm);
  Serial.println("cm");
  doStaff(cm); // All logic controller is implemented here
}

void doStaff(unsigned long distance) {
  char serIn = '0';
  if (Serial.available()) {
    serIn = Serial.read();
  }
  
  switch (serIn) {
    case 'w':
      if (distance <= 20) {
        stopMotor();
        delay(100);
      } else {
        Serial.println("Move robot forward");
        // move robot forward
        goForward();
      }
      break;
    case 's':
      Serial.println("Move robot backward");
      // move robot backward
      goBackward();
      break;
    case 'a':
      Serial.println("Move robot to left direction");
      // move robot to left direction
      goLeft();
      break;
    case 'd':
      Serial.println("Move robot to right direction");
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
  // Back Motor
  digitalWrite(int1B1, LOW);
  digitalWrite(int2B1, LOW);
  digitalWrite(int1B2, LOW);
  digitalWrite(int2B2, LOW);
  // Front Motor
  digitalWrite(int1F1, LOW);
  digitalWrite(int2F1, LOW);
  digitalWrite(int1F2, LOW);
  digitalWrite(int2F2, LOW);
}

void goBackward() {
  // Stop motor before change direction
  stopMotor();
  delay(100);
  // Left Motor
  digitalWrite(int1B1, HIGH);
  digitalWrite(int2B1, LOW);
  digitalWrite(int1F1, HIGH);
  digitalWrite(int2F1, LOW);
  // Right Motor
  digitalWrite(int1B2, LOW);
  digitalWrite(int2B2, HIGH);
  digitalWrite(int1F2, LOW);
  digitalWrite(int2F2, HIGH);
  delay(DELAY);
}

void goForward() {
  // Stop motor before change direction
  stopMotor();
  delay(100);
  // Left Motor
  digitalWrite(int1B1, LOW);
  digitalWrite(int2B1, HIGH);
  digitalWrite(int1F1, LOW);
  digitalWrite(int2F1, HIGH);
  // Right Motor
  digitalWrite(int1B2, HIGH);
  digitalWrite(int2B2, LOW);
  digitalWrite(int1F2, HIGH);
  digitalWrite(int2F2, LOW);
  delay(DELAY);
}

void goLeft() {
  // Stop motor before change direction
  stopMotor();
  delay(100);
  // Left Motor
  digitalWrite(int1B1, HIGH);
  digitalWrite(int2B1, LOW);
  digitalWrite(int1F1, HIGH);
  digitalWrite(int2F1, LOW);
  // Right Motor  
  digitalWrite(int1B2, HIGH);
  digitalWrite(int2B2, LOW);
  digitalWrite(int1F2, HIGH);
  digitalWrite(int2F2, LOW);
  delay(DELAY);
}

void goRight() {
  // Stop motor before change direction
  stopMotor();
  delay(100);
  // Left Motor
  digitalWrite(int1B1, LOW);
  digitalWrite(int2B1, HIGH);
  digitalWrite(int1F1, LOW);
  digitalWrite(int2F1, HIGH);
  // Right Motor
  digitalWrite(int1B2, LOW);
  digitalWrite(int2B2, HIGH);
  digitalWrite(int1F2, LOW);
  digitalWrite(int2F2, HIGH);
  delay(DELAY);
}

