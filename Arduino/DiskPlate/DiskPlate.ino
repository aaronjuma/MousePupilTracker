#include <Encoder.h>

Encoder disk(2, 3);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("Test:");
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
}

unsigned long prev = 0;
unsigned long curr = disk.read();
unsigned long prevT = 0;
unsigned long currT = millis();
bool signalSent = false;
unsigned long timeSinceSignal = 0;
bool potentialHigh = false;
unsigned long timer = 0;

void loop() {
  delay(20);
  prev = curr;
  curr = disk.read();
  prevT = currT;
  currT = millis();
  unsigned long speed = ((curr-prev)/4096.0)*1000.0/(currT-prevT); //revs/sec
//  Serial.println(abs(speed));

  if (signalSent == false){
    if (abs(speed) >= 3){
      if (potentialHigh == false){
        timer = millis();
        potentialHigh = true;
      }
      else{
        unsigned long timeDiff = (millis() - timer)/1000.0;
        if(timeDiff >= 5){
          signalSent = true;
          digitalWrite(13, HIGH);
          potentialHigh = false;
          timeSinceSignal = millis();
        }
      }
    }
    else{
      potentialHigh = false;
    }
  }
  else{
    unsigned long timeDiff = (millis() - timeSinceSignal)/1000.0;
    if(timeDiff >= 10){
      digitalWrite(13, LOW);
      signalSent = false;
      potentialHigh = false;
    }
  }
      
}
