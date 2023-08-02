from threading import Thread
import time

class Controller:
    def __init__(self, arduinoBoard):
        self.arduino = arduinoBoard
        self.t = Thread(target=self.run)
        self.t.daemon = True
        self.running = False

        # Parameters
        self.diameter = 0
        self.speed = 0
        self.speedThreshold = 1.7
        self.eyeThreshold = 1.0
        self.timeThreshold = 3.0
        self.timeSpeedActivate = 1.0

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def run(self):

        # Control Variables
        signalSent = False
        potential = False
        timer = 0
        timeSinceSignal = 0
        speedHigher = False
        timeElapsedSpeed = 0

        while True:
            if self.running == False:
                break

            # Condition to turn light ON
            if signalSent == False:
                # if (self.speed < self.speedThreshold and self.diameter >= self.eyeThreshold):
                if (self.speed < self.speedThreshold):
                    if potential == False:
                        timer = time.time()
                        potential = True
                    else:
                        timeDiff = time.time() - timer

                        if timeDiff >= self.timeThreshold:
                            signalSent = True
                            self.activate()
                            potential = False
                            timeSinceSignal = time.time()
                else:
                    potential = False
            else:
                timeDiff = time.time() - timeSinceSignal

                #Checks for pupil size condition
                # if self.diameter < self.eyeThreshold:
                #     self.deactivate()
                #     potential = False
                #     signalSent = False

                #Checks for speed condition
                if self.speed >= self.speedThreshold:
                    if speedHigher == False:
                        timeElapsedSpeed = time.time()
                        speedHigher = True
                    else:
                        timeDifference = time.time() - timeElapsedSpeed

                        if timeDifference >= self.timeSpeedActivate:
                            self.deactivate()
                            potential = False
                            signalSent = False

    def activate(self):
        self.arduino.write(1)

    def deactivate(self):
        self.arduino.write(0)

    def updateValues(self, pupilDiameter):
        self.diameter = pupilDiameter
        self.speed = self.arduino.read()
