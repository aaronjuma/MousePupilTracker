from threading import Thread
from datetime import date, datetime
import time

class Logger:
    def __init__(self):
        self.filename = ''
        self.data = 0
        self.t = Thread(target=self.writeData)
        self.t.daemon = True
        self.running = False
        self.startTime = 0
        
    def initialize(self):
        print("Beginning to log items...")
        self.filename = str(date.today())+'-'+datetime.now().strftime("%H-%M-%S")+'.csv'
        with open('Data/Logs/'+self.filename, 'w') as f:
            f.write('time,diameter\n')
        self.running = True
        self.startTime = time.time()
        self.t.start()
        
    def writeData(self):
        while True:
            if self.running == False:
                break
            x = round(time.time() - self.startTime, 1)
            y = self.data
            print(f'{x},{y}', file=open('Data/Logs/'+self.filename,'a')) 
            time.sleep(0.5)
            
    def update(self, data):
        self.data = data
            
    def stop(self):
        self.running = False
        