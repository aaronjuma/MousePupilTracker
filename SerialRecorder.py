import serial
import serial.tools.list_ports

class SerialRecorder:
    def __init__(self, baudrate = 9600, timeout=.1):
        self.board = None
        for p in serial.tools.list_ports.comports():
            if 'Arduino' in p.description:
                self.board = serial.Serial(port=p.device, baudrate=baudrate, timeout=timeout)
                break
        
    def status(self):
        if self.board == None:
            return False
        else:
            return True
    
    def write(self, data):
        self.board.write(data)
    
    def read(self):
        return self.board.readline().decode("utf-8")

