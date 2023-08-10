from threading import Thread
from datetime import date, datetime
import time
import os

class Logger:
    def __init__(self):
        self.direc = 'Data/Logs/'+str(date.today())+'-'+datetime.now().strftime("%H-%M-%S")+'/'
        self.type = ""
        self.pupil = 0
        self.speed = []
        self.sysStatus = 0

        self.t = Thread(target=self.writeData)
        self.t.daemon = True
        self.running = False
        self.startTime = 0
        
    def initialize(self, TYPE):
        if not os.path.exists(self.direc):
            os.makedirs(self.direc)

        self.type = TYPE
        if TYPE == "SAMPLE":
            self.filename = "Sample.csv"
            with open(self.direc+self.filename, 'w') as f:
                f.write('time,diameter\n')
        if TYPE == "TRIAL": 
            self.filename = "Trial.csv"
            with open(self.direc+self.filename, 'w') as f:
                f.write('time,diameter,system status\n')
        
        self.running = True
        self.startTime = time.time()
        self.t.start()
        
    def writeData(self):
        while True:
            if self.running == False:
                break
            x = round(time.time() - self.startTime, 1)

            if self.type == "SAMPLE":
                print(f'{x},{self.pupil}', file=open(self.direc+self.filename,'a')) 
            if self.type == "TRIAL":
                print(f'{x},{self.pupil},{self.sysStatus}', file=open(self.direc+self.filename,'a'))
                print(self.turnBinToString(self.speed), file=open(self.direc+'Speed.csv','a'))

            time.sleep(1)
            
    def update(self, pupil = 0, speed = 0, sysStatus = 0):
        self.pupil = pupil
        self.speed = speed
        self.sysStatus = sysStatus
            
    def stop(self):
        self.running = False
    
    def turnBinToString(self, bin):
        text = ''.join([str(x)+',' for x in bin])
        return text[:-1]