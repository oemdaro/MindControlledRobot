#include <NewPing.h>
#include <Servo.h>

#define SONAR_NUM      2 // Number of sensors.
#define MAX_DISTANCE 200 // Maximum distance (in cm) to ping.
#define PING_INTERVAL 33 // Milliseconds between sensor pings (29ms is about the min to avoid cross-sensor echo).

unsigned long pingTimer[SONAR_NUM]; // Holds the times when the next ping should happen for each sensor.
unsigned int cm[SONAR_NUM];         // Where the ping distances are stored.
uint8_t currentSensor = 0;          // Keeps track of which sensor is active.

// Declare L298N Dual H-Bridge Motor Controller directly since there is not a library to load.

// Motor A
uint8_t dir1PinA = 2;
uint8_t dir2PinA = 3;
int speedPinA = 4; // Needs to be a PWM pin to be able to control motor speed

// Motor B
uint8_t dir1PinB = 5;
uint8_t dir2PinB = 6;
int speedPinB = 7; // Needs to be a PWM pin to be able to control motor speed

const int servoPin = 6; // the digital pin used for the first servo

NewPing sonar[SONAR_NUM] = {     // Sensor object array.
  NewPing(22, 23, MAX_DISTANCE), // Each sensor's trigger pin, echo pin, and max distance to ping.
  NewPing(24, 25, MAX_DISTANCE),
};

Servo servo;  // create servo object to control a servo

void setup() {
  // initialize serial communication @ 115200 baud
  Serial.begin(115200);
  
  pinMode(dir1PinA,OUTPUT);
  pinMode(dir2PinA,OUTPUT);
  pinMode(speedPinA,OUTPUT);
  pinMode(dir1PinB,OUTPUT);
  pinMode(dir2PinB,OUTPUT);
  pinMode(speedPinB,OUTPUT);

  servo.attach(servoPin);  // attaches the servo on pin 9 to the servo object
  servo.write(0);
  pingTimer[0] = millis() + 75;           // First ping starts at 75ms, gives time for the Arduino to chill before starting.
  for (uint8_t i = 1; i < SONAR_NUM; i++) // Set the starting time for each sensor.
    pingTimer[i] = pingTimer[i - 1] + PING_INTERVAL;
}

void loop() {
  for (uint8_t angle = 15; angle <= 165; angle++) {
    // write servo angle position
    servo.write(angle);
    
    for (uint8_t i = 0; i < SONAR_NUM; i++) { // Loop through all the sensors.
      if (millis() >= pingTimer[i]) {         // Is it this sensor's time to ping?
        pingTimer[i] += PING_INTERVAL * SONAR_NUM;  // Set next time this sensor will be pinged.
        if (i == 0 && currentSensor == SONAR_NUM - 1) oneSensorCycle(); // Sensor ping cycle complete, do something with the results.
        sonar[currentSensor].timer_stop();          // Make sure previous timer is canceled before starting a new ping (insurance).
        currentSensor = i;                          // Sensor being accessed.
        cm[currentSensor] = 0;                      // Make distance zero in case there's no ping echo for this sensor.
        sonar[currentSensor].ping_timer(echoCheck); // Do the ping (processing continues, interrupt will call echoCheck to look for echo).
      }
    }

    // Other code that *DOESN'T* analyze ping results can go here.
    doStaff(); // All logic controller is implemented here
    delay(30); // delay for 30 ms
  }

  for (uint8_t angle = 165; angle > 15; angle--) {
    // write servo angle position
    servo.write(angle);

    // ping ultrasonic sensor
    for (uint8_t i = 0; i < SONAR_NUM; i++) { // Loop through all the sensors.
      if (millis() >= pingTimer[i]) {         // Is it this sensor's time to ping?
        pingTimer[i] += PING_INTERVAL * SONAR_NUM;  // Set next time this sensor will be pinged.
        if (i == 0 && currentSensor == SONAR_NUM - 1) oneSensorCycle(); // Sensor ping cycle complete, do something with the results.
        sonar[currentSensor].timer_stop();          // Make sure previous timer is canceled before starting a new ping (insurance).
        currentSensor = i;                          // Sensor being accessed.
        cm[currentSensor] = 0;                      // Make distance zero in case there's no ping echo for this sensor.
        sonar[currentSensor].ping_timer(echoCheck); // Do the ping (processing continues, interrupt will call echoCheck to look for echo).
      }
    }

    // Other code that *DOESN'T* analyze ping results can go here.
    doStaff(); // All logic controller is implemented here
    delay(30); // delay for 30 ms
  }
}

void echoCheck() { // If ping received, set the sensor distance to array.
  if (sonar[currentSensor].check_timer())
    cm[currentSensor] = sonar[currentSensor].ping_result / US_ROUNDTRIP_CM;
}

void oneSensorCycle() { // Sensor ping cycle complete, do something with the results.
  // The following code would be replaced with your code that does something with the ping results.
  for (uint8_t i = 0; i < SONAR_NUM; i++) {
    Serial.print(i);
    Serial.print("=");
    Serial.print(cm[i]);
    Serial.print("cm ");
  }
  Serial.println();
}

void doStaff() {
  uint8_t serIn = 0;
  if (Serial.available()) {
    serIn = Serial.read();
  }
  
  switch (serIn) {
    case 1:
      // move robot forward
      goForward();
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
      break;
  }
}

void goForward() {
  // move robot forward
}

void goBackward() {
  // move robot backward
}

void goLeft() {
  // move robot left direction
}

void goRight() {
  // move robot right direction
}

