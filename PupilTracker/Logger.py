"""
Logger.py
This class is responsible for logging all the data into files.
"""
from threading import Thread
from datetime import date, datetime
import time
import os

class Logger:

    """
    Initializer for the Logger Class
    Input: None
    Output: None
    """
    def __init__(self):

        # Creates a unique named folder
        self.direc = 'Data/Logs/'+str(date.today())+'-'+datetime.now().strftime("%H-%M-%S")+'/'

        # Variable for determing whether it is logging sample or trial
        self.type = ""

        # Variable for containing the data
        self.pupil = 0
        self.speed = []
        self.sysStatus = 0
        self.startTime = 0

        # Threading variable
        self.t = Thread(target=self.writeData)
        self.t.daemon = True
        self.running = False
    

    """
    Starts the logging 
    Input: None
    Output: None
    """
    def start(self):

        # If folder does not exist yet, create a directory for it
        if not os.path.exists(self.direc):
            os.makedirs(self.direc)
        
        # Starts the thread
        self.running = True
        self.startTime = time.time()
        self.t.start()
    

    """
    Stops the thread
    Input: None
    Output: None
    """
    def stop(self):
        self.running = False


    """
    Threaded function that will write the data onto the file
    Input: None
    Output: None
    """
    def writeData(self):
        while True:

            # Breaks the thread the the stop function is called
            if self.running == False:
                break

            # Updates the time variable
            x = round(time.time() - self.startTime, 1)

            # If it is in sample mode, it will log just the pupil to the 'Sample.csv' file
            if self.type == "SAMPLE":
                print(f'{x},{self.pupil}', file=open(self.direc+self.filename,'a')) 

            # If it is in trial mode, it will log the pupil size and the system status to the 'Sample.csv' file
            # It will log the speed bin in a seperate file called 'Speed.csv'
            if self.type == "TRIAL":
                print(f'{x},{self.pupil},{self.sysStatus}', file=open(self.direc+self.filename,'a'))
                print(self.turnBinToString(self.speed), file=open(self.direc+'Speed.csv','a'))

            # Updates every 1 seconds
            time.sleep(1)
            
    
    """
    Used by the main program to feed data to this class
    Input: Pupil size, Speed, and System Status
    Output: None
    """
    def update(self, pupil = 0, speed = 0, sysStatus = 0):
        self.pupil = pupil
        self.speed = speed
        self.sysStatus = sysStatus
    

    """
    Turns the bin into a string to be logged to the csv
    Input: Speed Bin
    Output: None
    """
    def turnBinToString(self, bin):
        # Turns bin into a string
        text = ''.join([str(x)+',' for x in bin])
        return text[:-1]
    

    """
    Gets the directory for the current data folder, Used by the ThresholdCalculator.py
    to calculate the mean and STD
    Input: None
    Output: Directory for the data folder
    """
    def getDirec(self):
        return self.direc
    

    """
    Used by the main program to set the different modes of logging.
    Input: The type, either 'SAMPLE' or 'TRIAL'
    Output: None
    """
    def setType(self, TYPE):

        # Updates the type
        self.type = TYPE

        # Creates a new file for sample
        if TYPE == "SAMPLE":
            self.filename = "Sample.csv"
            with open(self.direc+self.filename, 'w') as f:
                f.write('time,diameter\n')

        # Creates two new files for trial 
        if TYPE == "TRIAL": 
            self.filename = "Trial.csv"
            with open(self.direc+self.filename, 'w') as f:
                f.write('time,diameter,system status\n')
            with open(self.direc+'Speed.csv', 'w') as f:
                f.write('speedbin\n')