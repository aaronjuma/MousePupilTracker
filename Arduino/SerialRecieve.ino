bool status = false;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(.1);
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    // read the incoming byte:
    int incomingByte = Serial.readString().toInt();

    if (incomingByte == 1) {
      if (status == false) {
        digitalWrite(13, HIGH);
        status = true;
        Serial.print("ON");
      }
      else {
        digitalWrite(13, LOW);
        status = false;
        Serial.print("OFF");
      }
    }
  }
}
