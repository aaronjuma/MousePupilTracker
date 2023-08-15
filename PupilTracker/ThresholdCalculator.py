import numpy as np

class ThresholdCalculator:
    def __init__(self, direc):
        self.direc = direc
        self.mean = 0
        self.std = 0

    def run(self):
        arr=[] #creating the array
        arr = np.loadtxt(self.direc+"Sample.csv",
                        delimiter=",", skiprows = 1, dtype=float)
        x=arr[:,1]
        self.mean = np.mean(x)
        self.std = np.std(x)
        with open(self.direc+"ThresholdParams.txt", 'w') as f:
            f.write(f'MEAN: {self.mean}\n')
            f.write(f'STD: {self.std}')

    def getMean(self):
        return self.mean
    
    def getSTD(self):
        return self.std