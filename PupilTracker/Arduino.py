"""
Arduino.py
This class is responsible for recieving and sending data to and from
the arduino. It automatically looks at each serial port and sets up an
arduino object. It then starts a daemon thread that will run in the background
constantly receiving data from the arduino. The data is saved in a variable called 
data, and the history of speed is saved in a bin.
"""

import serial
import serial.tools.list_ports
import time
from threading import Thread

class Arduino:

    """
    Initializer for the Arduino Class
    Input: No need to input
    Output: None
    """
    def __init__(self, baudrate = 19200, timeout = .1):
        self.board = None

        # Loops through the serial to see if there is an arduino
        for p in serial.tools.list_ports.comports():
            if 'Arduino' in p.description:
                self.board = serial.Serial(port=p.device, baudrate=baudrate, timeout = timeout)
                break
        
        # Threading variables
        self.t = Thread(target=self.read)
        self.t.daemon = True
        self.running = False

        # Data Variables
        self.data = 0
        self.bin = []
    

    """
    Checks the status of the arduino if there exists an arduino
    Input: None
    Output: True if there is arduino, False if there is no arduino
    """
    def status(self):
        if self.board == None:
            return False
        else:
            return True
    

    """
    Starts the thread for the Arduino to concurrently get the data in the background
    Input: None
    Output: True if there is arduino, False if there is no arduino
    """
    def start(self):
        self.running = True
        self.t.start()


    """
    Stops the thread of the Arduino
    Input: None
    Output: None
    """
    def stop(self):
        self.running = False


    """
    The threaded function, Loops to constantly updates values of the speed and stores
    it in the variable 'data' and 'bin'
    Input: None
    Output: None
    """
    def read(self):

        # Clears the previous input
        self.board.flushInput()

        # Time Variable
        prevTime = 0
        currTime = time.time()


        while True:

            # Breaks the thread if the stop function is called
            if self.running == False:
                break

            # Gets the value from the arduino
            try:
                value = self.board.readline().decode("utf-8")

            # Sometimes the arduino will randomly spit weird values, dont want to crash
            except (UnicodeDecodeError, AttributeError):
                value = 0
                pass

            # Updates the speed value
            self.data = float(value) if self.isFloat(value) else 0.0
            
            # Logs the speed value to a bin every 10 ms
            prevTime = currTime
            currTime = time.time()
            if currTime - prevTime > 0.01: # Every 0.01s (10ms)

                # Adds the time to the array and trims to just 100 items (roughly 1 seconds worth of data)
                self.bin.append(self.data)
                self.bin = self.bin[-100:]
    

    """
    Gets the value of the speed (Used for the main program)
    Input: None
    Output: Speed value
    """
    def getValue(self):
        return self.data
    

    """
    Writes a message to the arduino (Tells it to activate or not)
    Input: Value (1 or 0)
    Output: None
    """
    def write(self, value):
        self.board.write(str(value).encode())
    

    """
    Checks if something is a float (when recieving arduino data)
    Input: Value (Raw arduino data)
    Output: True if value is float, False if it is not float
    """
    def isFloat(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False
    
    """
    Gets the bin data (Used for the Logger)
    Input: None
    Output: Returns the bin array
    """
    def getBin(self):
        return self.bin[-100:]

