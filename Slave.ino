#include <AccelStepper.h>
#include <Wire.h>


// ULN2003 + 28BYJ-48 pin order
AccelStepper stepper1(AccelStepper::FULL4WIRE, 0,2,1,3);
AccelStepper stepper2(AccelStepper::FULL4WIRE, 4,6,5,7);
AccelStepper stepper3(AccelStepper::FULL4WIRE, 8,10,9,11);

int active_stepper = 1;
char hhbyte, hlbyte, lhbyte, llbyte;
int value;


unsigned long target1 = 0;
unsigned long target2 = 0;
unsigned long target3 = 0;

void setup() {
  //Serial.begin(9600);
  //Serial.println("HELLO");

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);


  Wire.begin(3);
  Wire.onReceive(requestEvent);

  pinMode(LED_BUILTIN, OUTPUT);
  stepper1.setMaxSpeed(600);       
  stepper1.setAcceleration(200);   
  stepper2.setMaxSpeed(600);       
  stepper2.setAcceleration(200); 
  stepper3.setMaxSpeed(600);       
  stepper3.setAcceleration(200); 

  delay(100);
  stepper1.moveTo(target1);
  stepper2.moveTo(target2);
  stepper3.moveTo(target3);
}

void requestEvent() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(50);
  digitalWrite(LED_BUILTIN, LOW);
  
  hhbyte = Wire.read();
  hlbyte = Wire.read();
  lhbyte = Wire.read();
  llbyte = Wire.read();
  value = (hhbyte << 24) | (hlbyte << 16) | (lhbyte << 8) | (llbyte);
  
  //Serial.println(value);
  if (active_stepper == 1) {
    target1 = value;
    active_stepper = 2;
  } else if (active_stepper == 2) {
    target2 = value;
    active_stepper = 3;
  } else {
    target3 = value;
    active_stepper = 1;
  }

}


void loop() {

  stepper1.moveTo(target1);
  stepper2.moveTo(target2);
  stepper3.moveTo(target3);

  stepper1.run();                  // must run continuously
  stepper2.run();
  stepper3.run();
}

