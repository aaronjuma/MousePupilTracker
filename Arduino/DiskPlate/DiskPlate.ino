/*
Arduino Sketch for Activating TTL based on Disk Velocity
*/
#include <Encoder.h>

Encoder disk(2, 3); //Encoder object to read values from plate

//PARAMETERS TO CHANGE
double speedThreshold = 2; //Threshold the speed must be below to activate system (revs/sec)
unsigned long timeThreshold = 5; //Amount of time needed for speed to be below threshold to activate system
unsigned long activationTime = 4;
unsigned long cooldown = 10; //Amount of time needed to wait before system can activate again
float frequency = 30;

//Logic Variables
long prev = 0;
long curr = disk.read();
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
  double diskSpeed = ((curr-prev)/4096.0)*(1000.0/(currT-prevT)); //revs/sec

  Serial.println(diskSpeed);

  //Checks if a signal hasn't been sent already
  if (signalSent == false){

    //Checks if speed hit threshold
    if (abs(diskSpeed) >= speedThreshold){

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
    if(timeDiff >= cooldown){
      signalSent = false;
      potentialHigh = false;
    }
  }
      
}



//Code for activating system (NEEDS CHANGE FOR TTL)
void activate() {
  unsigned long startTime = millis();
  unsigned long timeDiff = 0;
  double timeDelay = (1000.0/frequency)/2;
  
  while (timeDiff < activationTime*1000){
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
    delay(timeDelay);                       // wait for a second
    digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
    delay(timeDelay);                       // wait for a second
    timeDiff = (millis()-startTime);
  }
}
