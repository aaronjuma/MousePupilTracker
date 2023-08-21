"""
ThresholdCalculator.py
This class is responsible for calculating the threshold by
getting the Sample data and calculatin the standard deviation and mean.
"""

import numpy as np

class ThresholdCalculator:

    """
    Initializes the ThresholdCalculator Class
    Input: Directory for the folder (from Logger.py)
    Output: None
    """
    def __init__(self, direc):
        self.direc = direc
        self.mean = 0
        self.std = 0


    """
    Function that will open up the file, read the data, and calculate mean and std
    Input: None
    Output: None
    """
    def run(self):

        # Array for storing data points
        arr=[] 

        # Loads the Sample data onto the array
        arr = np.loadtxt(self.direc+"Sample.csv",
                        delimiter=",", skiprows = 1, dtype=float)
        
        # Uses only the second column
        x=arr[:,1]

        # Calculates the mean and std
        self.mean = np.mean(x)
        self.std = np.std(x)

        # Creates a new file to store the std and mean
        with open(self.direc+"ThresholdParams.txt", 'w') as f:
            f.write(f'MEAN: {self.mean}\n')
            f.write(f'STD: {self.std}')


    """
    Returns the mean value for the main program
    Input: None
    Output: Mean Value
    """
    def getMean(self):
        return self.mean


    """
    Returns the standard deviation value for the main program
    Input: None
    Output: Standard Deviation value
    """
    def getSTD(self):
        return self.std