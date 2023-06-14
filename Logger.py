from threading import Thread
import time

class Logger:
    def __init__(self):
        self.filename = ''
        self.data = 0
        self.t = Thread(target=self.writeData)
        self.t.daemon = True
        self.running = False
        self.startTime = 0
        
    def initialize(self, filename):
        self.filename = filename
        with open(self.filename, 'w') as f:
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
            print(f'{x},{y}', file=open(self.filename,'a')) 
            time.sleep(0.5)
            
    def update(self, data):
        self.data = data
            
    def stop(self):
        self.running = False
        