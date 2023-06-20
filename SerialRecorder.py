import struct
import serial
import serial.tools.list_ports
import time
from threading import Thread

class SerialRecorder:
    def __init__(self, baudrate = 9600, timeout = .1):
        self.board = None
        for p in serial.tools.list_ports.comports():
            if 'Arduino' in p.description:
                self.board = serial.Serial(port=p.device, baudrate=baudrate, timeout = timeout)
                break
        self.data = 0
        self.isRunning = False
        self.t = Thread(target = self.write)
        self.t.daemon = True
        
    def status(self):
        if self.board == None:
            return False
        else:
            return True
    
    def run(self):
        self.isRunning = True
        self.t.start()
    
    def write(self):
        while True:
            if self.isRunning == False:
                break
            self.board.write(str(self.data).encode())
            time.sleep(0.5)
    
    def update(self, value):
        self.data = int(value)
            
    def stop(self):
        self.isRunning = False
        self.board.close()
    
    def read(self):
        return self.board.readline().decode("utf-8")

