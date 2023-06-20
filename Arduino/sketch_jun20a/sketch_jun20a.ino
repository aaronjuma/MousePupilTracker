void setup() {
  Serial.begin(9600);
  Serial.setTimeout(100);
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
}

int val = 70;
void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()){
    String incomingByte = Serial.readString();
    val = incomingByte.toInt();
  }

  if (val >= 60) {
    digitalWrite(13, HIGH);
    delay(5000);
  }
  else {
    digitalWrite(13, LOW);
  }
}
