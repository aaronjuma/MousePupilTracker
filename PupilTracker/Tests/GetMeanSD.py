import numpy as np

arr=[] #creating the array


arr = np.loadtxt("Data/Logs/2023-08-02-15-10-25.csv",
                 delimiter=",", skiprows = 1, dtype=float)

x=arr[:,1]

mean = np.mean(x)
std = np.std(x)
print(mean)
print(std)