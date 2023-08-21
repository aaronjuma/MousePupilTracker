"""
Controller.py
This class is responsible for controlling the whole closed loop system.
It will recieves inputs about the speed and pupil size and will determine if
it should activate or not.
"""
from threading import Thread
import time

class Controller:

    """
    Initializes the Controller Class
    Input: Arduino Board (from Arduino class), config file
    Output: None
    """
    def __init__(self, arduinoBoard, config):

        # Get the arduino to be able to send messages to arduino
        self.arduino = arduinoBoard

        # Threading variables
        self.t = Thread(target=self.run)
        self.t.daemon = True
        self.running = False
        self.signalSent = False

        # Parameters
        self.diameter = 0
        self.speed = 0
        self.speedThreshold = config["SPEED_THRESHOLD"]
        self.eyeThreshold = config["EYE_THRESHOLD"]
        self.activationTime = config["ACTIVATION_TIME"]
        self.deactivationTime = config["DEACTIVATION_TIME"]
        self.mean = 0
        self.std = 1


    """
    Starts the controller thread
    Input: The mean and standard deviation from the sampling period
    Output: None
    """
    def start(self, mean, std):

        #Updates values
        self.mean = mean
        self.std = std

        # Starts the thread
        self.running = True
        self.t.start()


    """
    Stops the thread
    Input: None
    Output: None
    """
    def stop(self):
        self.running = False


    """
    The threaded function, a loop that will activate or deactivate the system based 
    on the speed and pupil size
    Input: None
    Output: None
    """
    def run(self):
        # Control Variables
        self.signalSent = False
        potential = False
        timer = 0
        timeSinceSignal = 0
        speedHigher = False
        timeElapsedSpeed = 0

        # The loop
        while True:
            
            # Added a sleep to make things run better
            time.sleep(0.01)

            # Breaks the loop when the stop function is called
            if self.running == False:
                break

            # Performs Z-score calculation on the diameter
            diam = (self.diameter-self.mean)/self.std


            # Condition to turn light ON
            if self.signalSent == False:

                # Checks if the speed reached the threshold and if the diameter reached its threshold
                if (self.speed < self.speedThreshold and diam >= self.eyeThreshold):

                    # If it is the first time reaching the threshold, starts a timer
                    if potential == False:
                        timer = time.time()
                        potential = True

                    # If it is not the first time reaching the threshold, checks if it reached the time limit
                    else:

                        # Updates time
                        timeDiff = time.time() - timer

                        # Checks it the timer has been reached
                        if timeDiff >= self.activationTime:

                            # Activates the system
                            self.signalSent = True
                            self.activate()
                            print("activated")
                            potential = False
                            timeSinceSignal = time.time()

                # If the condition changed, timer is reset
                else:
                    potential = False

            # Condition to turn light OFF
            else:
                timeDiff = time.time() - timeSinceSignal

                # Checks for pupil size condition
                if diam < self.eyeThreshold:

                    # Deactives the system
                    self.deactivate()
                    print("deactive")
                    potential = False
                    self.signalSent = False

                #Checks for speed condition
                if abs(self.speed) >= self.speedThreshold:

                    # If it is the first time, start a timer
                    if speedHigher == False:
                        timeElapsedSpeed = time.time()
                        speedHigher = True

                    # If it is not the first time, check the timer
                    else:
                        timeDifference = time.time() - timeElapsedSpeed
                        
                        # If the timer reached the goal
                        if timeDifference >= self.deactivationTime:

                            # Deactivates the system
                            print("deactive")
                            self.deactivate()
                            potential = False
                            self.signalSent = False
                            speedHigher = False

                # Resets the timer if speed condition is not reached
                else:
                    speedHigher = False


    """
    Activates the system by sending the signal to the arduino
    for a TTL pulse
    Input: None
    Output: None
    """
    def activate(self):
        self.arduino.write(1)


    """
    Deactivates the system by send the signal to the arduino
    to prevent a TTL pulse
    Input: None
    Output: None
    """
    def deactivate(self):
        self.arduino.write(0)


    """
    Used by the main program to update the data variales
    Input: Pupil size and Speed
    Output: None
    """
    def updateValues(self, pupilDiameter, speed):
        self.diameter = pupilDiameter
        self.speed = speed
    

    """
    Used by the logger to see if the system is on or off
    Input: None
    Output: 1 if the system is on, 0 if the system is off
    """
    def getStatus(self):
        return 0 if self.signalSent == False else 1
