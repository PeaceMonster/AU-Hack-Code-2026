#include <Wire.h>

char hhbyte, hlbyte, lhbyte, llbyte;
int target_val = 0;
int target_slave = 1;
int target_motor = 1;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Wire.begin();
}

void send_int(int n, int s) {
  hhbyte = (n >> 24) & 0xFF;
  hlbyte = (n >> 16) & 0xFF;
  lhbyte = (n >> 8) & 0xFF;
  llbyte = n & 0xFF;
  Wire.beginTransmission(s);
  Wire.write(hhbyte);
  Wire.write(hlbyte);
  Wire.write(lhbyte);
  Wire.write(llbyte);
  Wire.endTransmission();
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()) {
    target_val = Serial.parseInt();
    if (target_val != 0) {
      Serial.println(target_slave);
      send_int(target_val, target_slave);
      target_motor++;
      if (target_motor > 3) {
        target_motor = 1;
        target_slave++;
      }
      if (target_slave > 3) {
        target_slave = 1;
      }
    }
    
  }
}
