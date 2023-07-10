/*
Arduino Sketch for Activating TTL based on Eye Pupil Size
*/


//PARAMTERS TO CHANGE
unsigned long eyeThreshold = 1.0; //Diameter of the eye (mm) required to activate system
unsigned long timeThreshold = 5; //How much time (seconds) the eye has to stay past the threshold to activate
unsigned long cooldown = 10; //How much time before activating system again after activating

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(100);
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
}

bool signalSent = false;
unsigned long timeSinceSignal = 0;
bool potentialHigh = false;
unsigned long timer = 0;
float val = 0;

void loop() {

  // Checks if we got a signal from the computer
  if(Serial.available()){
    String incomingByte = Serial.readString();
    val = incomingByte.toFloat();
  }


  if (signalSent == false){
    if (val >= eyeThreshold){
      if (potentialHigh == false){
        timer = millis();
        potentialHigh = true;
      }
      else{
        unsigned long timeDiff = (millis() - timer)/1000.0;
        if(timeDiff >= timeThreshold){
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
    if(timeDiff >= cooldown){ //10 seconds
      digitalWrite(13, LOW);
      signalSent = false;
      potentialHigh = false;
    }
  }
      
}