"""
ThresholdCalculator.py
This module is responsible for calculating the threshold by
getting the Sample data and calculatin the standard deviation and mean.
"""

import numpy as np

"""
Function that will open up the file, read the data, and calculate mean and std
Input: None
Output: None
"""
def getThresholdParams(direc):

    # Array for storing data points
    arr=[] 

    # Loads the Sample data onto the array
    arr = np.loadtxt(direc+"Sample.csv",
                    delimiter=",", skiprows = 1, dtype=float)
    
    # Uses only the second column
    x=arr[:,1]

    # Calculates the mean and std
    mean = np.mean(x)
    std = np.std(x)

    # Creates a new file to store the std and mean
    with open(direc+"ThresholdParams.txt", 'w') as f:
        f.write(f'MEAN: {mean}\n')
        f.write(f'STD: {std}')

    return mean, std
