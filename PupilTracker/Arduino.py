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
        self.t = Thread(target=self.read)
        self.t.daemon = True
        self.running = False
        self.data = 0
        self.bin = []
        
    def status(self):
        if self.board == None:
            return False
        else:
            return True
    
    def start(self):
        self.running = True
        self.t.start()

    def stop(self):
        self.running = False

    def read(self):
        self.board.flushInput()
        prevTime = time.time()
        while True:
            if self.running == False:
                break
            value = self.board.readline().decode("utf-8")
            self.data = float(value) if self.isFloat(value) else 0.0
            
            
            currTime = time.time()
            if currTime - prevTime > 0.01:
                self.bin.append(self.data)
                self.bin = self.bin[-100:]
    
    def getValue(self):
        return self.data
    
    def write(self, value):
        self.board.write(str(value).encode())
    
    def isFloat(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False
        
    def getBin(self):
        return self.bin

