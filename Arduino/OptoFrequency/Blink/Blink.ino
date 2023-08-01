void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
}

float frequency = 30;
double timeDelay = (1000.0/frequency)/2;
float val = 0;

void loop() {
  if(Serial.available()) {
    String incomingByte = Serial.readString();
    val = incomingByte.toFloat();
  }

  if (val == 1){
    unsigned long startTime = millis();
    unsigned long timeDiff = 0;
    int count = 0;
    
    while (timeDiff < 10000){
      digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
      delay(timeDelay);                       // wait for a second
      digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
      delay(timeDelay);                       // wait for a second
      timeDiff = (millis()-startTime);
      count++;
      Serial.println(count);
    }
    val = 0;
    count = 0;
  }
}
