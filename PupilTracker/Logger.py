from threading import Thread
from datetime import date, datetime
import time

class Logger:
    def __init__(self):
        self.filename = ''
        self.pupil = 0
        self.speed = 0
        self.t = Thread(target=self.writeData)
        self.t.daemon = True
        self.running = False
        self.startTime = 0
        
    def initialize(self):
        print("Beginning to log items...")
        self.filename = str(date.today())+'-'+datetime.now().strftime("%H-%M-%S")+'.csv'
        with open('Data/Logs/'+self.filename, 'w') as f:
            f.write('time,diameter, speed\n')
        self.running = True
        self.startTime = time.time()
        self.t.start()
        
    def writeData(self):
        while True:
            if self.running == False:
                break
            x = round(time.time() - self.startTime, 1)
            print(f'{x},{self.pupil},{self.speed}', file=open('Data/Logs/'+self.filename,'a')) 
            time.sleep(1)
            
    def update(self, pupil, speed):
        self.pupil = pupil
        self.speed = speed
            
    def stop(self):
        self.running = False
        