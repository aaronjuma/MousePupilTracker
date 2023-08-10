from threading import Thread
import time
import keyboard

class Controller:
    def __init__(self, arduinoBoard, config):
        self.arduino = arduinoBoard
        self.t = Thread(target=self.run)
        self.t.daemon = True
        self.running = False
        self.signalSent = False

        # Parameters
        mouseNumber = str(config["Mouse"])
        self.diameter = 0
        self.speed = 0
        self.speedThreshold = config["SPEED_THRESHOLD"]
        self.eyeThreshold = config["Mice"]["Mouse"+mouseNumber]["MEAN"]+config["Mice"]["Mouse"+mouseNumber]["STD"]
        self.timeThreshold = config["TIME_THRESHOLD"]
        self.timeSpeedActivate = config["SPEED_TIME_ACTIVATION"]

    def start(self):
        self.running = True
        self.t.start()

    def stop(self):
        self.running = False

    def run(self):
        # Control Variables
        self.signalSent = False
        potential = False
        timer = 0
        timeSinceSignal = 0
        speedHigher = False
        timeElapsedSpeed = 0

        while True:
            time.sleep(0.01)
            if self.running == False:
                break

            # Condition to turn light ON
            if self.signalSent == False:
                if (self.speed < self.speedThreshold and self.diameter >= self.eyeThreshold):
                # if (abs(self.speed) < self.speedThreshold):
                    if potential == False:
                        timer = time.time()
                        potential = True
                    else:
                        timeDiff = time.time() - timer

                        if timeDiff >= self.timeThreshold:
                            self.signalSent = True
                            self.activate()
                            print("activated")
                            potential = False
                            timeSinceSignal = time.time()
                else:
                    potential = False
            else:
                timeDiff = time.time() - timeSinceSignal

                # Checks for pupil size condition
                if self.diameter < self.eyeThreshold:
                    self.deactivate()
                    potential = False
                    self.signalSent = False

                #Checks for speed condition
                if abs(self.speed) >= self.speedThreshold:
                    if speedHigher == False:
                        timeElapsedSpeed = time.time()
                        speedHigher = True
                    else:
                        timeDifference = time.time() - timeElapsedSpeed
                        
                        if timeDifference >= self.timeSpeedActivate:
                            print("deactive")
                            self.deactivate()
                            potential = False
                            self.signalSent = False
                            speedHigher = False
                else:
                    speedHigher = False

    def activate(self):
        self.arduino.write(1)

    def deactivate(self):
        self.arduino.write(0)

    def updateValues(self, pupilDiameter, speed):
        self.diameter = pupilDiameter
        self.speed = speed
    
    def getStatus(self):
        return 0 if self.signalSent == False else 1
