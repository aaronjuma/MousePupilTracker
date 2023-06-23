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
int val = 0;

void loop() {
  if(Serial.available()){
    String incomingByte = Serial.readString();
    val = incomingByte.toInt();
  }

  if (signalSent == false){
    if (val >= 50){
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