import serial
import serial.tools.list_ports

class SerialRecorder:
    def __init__(self, baudrate=9600, timeout=.1):
        
        #Search for arduino
        ard = None
        for p in serial.tools.list_ports.comports():
            if 'Arduino' in p.description:
                ard = p.device
        
        if ard == None:
            print("No Arduino Found...")
        else:
            print("Arduino found in " + ard)
            self.board = serial.Serial(port=ard, baudrate=baudrate, timeout=timeout)
    
    def write(self, data):
        self.board.write(bytes(data, 'utf-8'))
    
    def read(self):
        return self.board.readline().decode("utf-8")

