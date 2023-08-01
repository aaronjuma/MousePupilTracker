/*
Arduino Sketch for Activating TTL based on Eye Pupil Size
*/

//PARAMTERS TO CHANGE
unsigned long eyeThreshold = 1.0; //Diameter of the eye (mm) required to activate system
unsigned long timeThreshold = 5; //How much time (seconds) the eye has to stay past the threshold to activate
unsigned long activationTime = 10; //How much time will the system activate for
unsigned long cooldown = 20;
float frequency = 30;

//Logic Variables
bool signalSent = false;
unsigned long timeSinceSignal = 0;
bool potentialHigh = false;
unsigned long timer = 0;
float val = 0;
bool activeSystem = false;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(100);
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
}

void loop() {
  // Checks if we got a signal from the computer
  if(Serial.available()){
    String incomingByte = Serial.readString();
    val = incomingByte.toFloat();
  }

  //Checks if we recently send a signal
  if (signalSent == false){

    //Checks if the current pupil size meets threshold
    if (val >= eyeThreshold){

      //Checks if it is the first time the pupil size hit the threshold
      if (potentialHigh == false){
        timer = millis();
        potentialHigh = true;
      }

      //Checks if the pupil size has already hit the threshold
      else{
        unsigned long timeDiff = (millis() - timer)/1000.0;

        //Checks if the time elapsed since first hitting the threshold has reached the time threshold
        if(timeDiff >= timeThreshold){
          signalSent = true;
          activate();
          potentialHigh = false;
          timeSinceSignal = millis();
        }
      }
    }

    //Checks if the current pupil size has not met the threshold (resets the timer)
    else{
      potentialHigh = false;
    }
  }

  //If the signal has already been sent
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
