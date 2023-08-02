import struct
import serial
import serial.tools.list_ports
import time
from threading import Thread

class Arduino:
    def __init__(self, baudrate = 19200, timeout = .1):
        self.board = None
        for p in serial.tools.list_ports.comports():
            if 'Arduino' in p.description:
                self.board = serial.Serial(port=p.device, baudrate=baudrate, timeout = timeout)
                break
        
    def status(self):
        if self.board == None:
            return False
        else:
            return True
    
    def read(self):
        # self.board.write(str(self.data).encode())
        value = self.board.readline().decode("utf-8")
        data = float(value) if self.isFloat(value) else 0.0
        return data
    
    def write(self, value):
        self.board.write(str(value).encode())
    
    def isFloat(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False

