/*
Arduino Sketch for Activating TTL based on Disk Velocity
*/
#include <Encoder.h>

Encoder disk(2, 3); //Encoder object to read values from plate

int timeOn = 10; //10 ms on
int timeOff = 90; //90 ms off
float radius = 3.0;

//Logic Variables
long prev = 0;
long curr = disk.read();
unsigned long prevT = 0;
unsigned long currT = millis();
unsigned long timeSinceSignal = 0;
int val = 0;
char speedVal[7];

void setup() {
  // put your setup code here, to run once:
  Serial.begin(19200);
  Serial.setTimeout(100);
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
  pinMode(11, OUTPUT);
  digitalWrite(11, HIGH);
}

void loop() {
  
  if(Serial.available()){
    String incomingByte = Serial.readString();
    val = incomingByte.toInt();
  }
  
  //Calculates the velocity
  prev = curr;
  curr = disk.read();
  prevT = currT;
  currT = millis();
  double diskSpeed = -(curr-prev)*1000.0*(2.0*3.14*radius) / (4096.0*(currT-prevT));
  dtostrf(diskSpeed, 4, 2, speedVal);
  Serial.println(speedVal);


  if (val == 1) {
    digitalWrite(13, HIGH);
    delay(timeOn);
    digitalWrite(13, LOW);
    delay(timeOff);
  }
  else{
    digitalWrite(13, LOW);
  }
}