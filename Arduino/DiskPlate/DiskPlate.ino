/*
Arduino Sketch for Activating TTL based on Disk Velocity
*/
#include <Encoder.h>

Encoder disk(2, 3); //Encoder object to read values from plate

//PARAMETERS TO CHANGE
unsigned long speedThreshold = 3; //Threshold the speed must be below to activate system (revs/sec)
unsigned long timeThreshold = 5; //Amount of time needed for speed to be below threshold to activate system
unsigned long cooldown = 10; //Amount of time needed to wait before system can activate again

//Logic Variables
unsigned long prev = 0;
unsigned long curr = disk.read();
unsigned long prevT = 0;
unsigned long currT = millis();
unsigned long timeSinceSignal = 0;
unsigned long timer = 0;
bool signalSent = false;
bool potentialHigh = false;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("Test:");
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
}

void loop() {
  delay(20); //Added delay for better encoder calculations

  //Calculates the velocity
  prev = curr;
  curr = disk.read();
  prevT = currT;
  currT = millis();
  unsigned long speed = ((curr-prev)/4096.0)*1000.0/(currT-prevT); //revs/sec

  //Checks if a signal hasn't been sent already
  if (signalSent == false){

    //Checks if speed hit threshold
    if (abs(speed) >= speedThreshold){

      //Checks if the it is first time hitting threshold
      if (potentialHigh == false){
        timer = millis();
        potentialHigh = true;
      }

      //Checks if the threshold has already been hit
      else{
        unsigned long timeDiff = (millis() - timer)/1000.0;

        //Checks if the threshold has been hit for a certain time
        if(timeDiff >= timeThreshold){
          signalSent = true;
          activate();
          potentialHigh = false;
          timeSinceSignal = millis();
        }
      }
    }

    //Checks if speed hasn't hit the threshold
    else{
      potentialHigh = false;
    }
  }

  //Checks if the signal has been sent
  else{
    unsigned long timeDiff = (millis() - timeSinceSignal)/1000.0;

    //Checks if the the cooldown has passed and is ready to send a signal again
    if(timeDiff >= 10){
      deactivate();
      signalSent = false;
      potentialHigh = false;
    }
  }
      
}

//Code for activating system (NEEDS CHANGE FOR TTL)
void activate() {
  digitalWrite(13, HIGH);
}

void deactivate() {
  digitalWrite(13, LOW);
}