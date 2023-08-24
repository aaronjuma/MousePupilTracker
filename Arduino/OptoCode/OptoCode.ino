/*
Arduino Sketch for Activating TTL based on Disk Velocity
*/
#include <Encoder.h>

Encoder disk(2, 3); //Encoder object to read values from plate

/*CHANGEABLE PARAMETERS*/
int timeOn = 10; //10 ms on
int timeOff = 90; //90 ms off
float radius = 3.0;


/*DO NOT CHANGE PARAMETERS*/
//Logic Variables for the Disk Calculations
long prev = 0; //Previous recording of disk position
long curr = disk.read(); //Current recording of disk position
unsigned long prevT = 0; //Previous time stamp
unsigned long currT = micros(); //Current time stamp
char speedVal[7]; //String to hold the speed value to send to the computer

//Logic Variables for the Stimulation
bool isOn = false; //Check if the system is actually on or not
bool active = false; //Check if the system was activated by computer
unsigned long timeSinceOn = 0;  //Time since it was first turned on
unsigned long timeSinceOff = 0; //Time since it was first turned off
int val = 0; //Value containing which mode to use


void setup() {
  // Setup code
  Serial.begin(19200); 
  Serial.setTimeout(100);

  //For the TTL Pulse
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);

  //For the lamp
  pinMode(11, OUTPUT);
  digitalWrite(11, HIGH);
}



void loop() {

  //Reads the value from the computer if there is any
  if(Serial.available()){
    String incomingByte = Serial.readString();
    val = incomingByte.toInt();
  }
  
  /*Calculates the velocity*/

  //First get the values
  prev = curr;
  curr = disk.read();
  prevT = currT;
  currT = micros();

  //Calculate the speed
  double diskSpeed = -(curr-prev)*1000000.0*(2.0*3.14*radius) / (4096.0*(unsigned long)(currT-prevT));

  //Convert number to string to send to computer
  dtostrf(diskSpeed, 4, 2, speedVal);

  //Send to computer
  Serial.println(speedVal);



  /* Controls the firing of TTL*/

  //Checks if computer wants to send TTL Pulse
  if (val == 1) {

    //Checks if it is the first time sending TTL Pulse to start pulse train
    if (active == false){
      active = true;
      isOn = true;
      digitalWrite(13, HIGH);
      timeSinceOn = millis();
    }

    //If it is not the first time sending TTL Pulse
    else{
      //If the signal is currently high
      if (isOn == true) {

        //Checks if it has reached the timeOn duration
        if(millis() - timeSinceOn > timeOn){

          //Set pulse to low
          isOn = false;
          digitalWrite(13, LOW);
          timeSinceOff = millis();
        }
      }

      //If the pulse is currently low
      else{

        // Checks if it has reached the timeOff duration
        if(millis() - timeSinceOff > timeOff) {

          //Set the pulse to high
          isOn = true;
          digitalWrite(13, HIGH);
          timeSinceOn = millis();
        }
      }
    }
  }

  //If the computer does not want to send TTL Pulse
  else{

    //Set pulse to low
    digitalWrite(13, LOW);

    //Resets the train
    active = false;
  }
}
