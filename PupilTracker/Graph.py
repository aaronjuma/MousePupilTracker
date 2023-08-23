"""
Graph.py
This class is responsible graphing the speed value, the pupil value,
and the pupil threshold value live.
"""
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Graph:

    """
    Initializer for the Grapher Class
    Input: config
    Output: None
    """
    def __init__(self, config):
        
        # Sets up the figure
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax2 = self.ax.twinx()

        # Log of Values 
        self.xs = []
        self.ys_speed = []
        self.ys_diameter = []

        # Individual data variables
        self.diameter = 0
        self.speed = 0
        self.thresh = []
        self.threshValue = 0

        # Gets config file and starts time
        self.config = config
        self.start_time = time.time()


    """
    Animate function that will update the graph with new values
    Input: None
    Output: None
    """
    def animate(self, i):

        # Appends the current values onto the log arrays
        self.xs.append(round(time.time() - self.start_time, 1))
        self.ys_diameter.append(self.diameter.value)
        self.ys_speed.append(self.speed.value)
        
        # Crops the log arrays to get the last 100 instances (25 seconds of data)
        self.xs = self.xs[-100:]
        self.ys_diameter = self.ys_diameter[-100:]
        self.ys_speed = self.ys_speed[-100:]

        # Updates the Pupil Size Graph
        self.ax.clear()
        self.ax.set_xlabel('Time (s)')

        # Checks if a new threshold has been made
        if np.isnan(self.thresh[0]) and np.isnan(self.thresh[1]):
            self.ax.set_ylabel('Eye Diameter (pixels)', color='tab:red', labelpad=15)
            self.ax.plot(self.xs, self.ys_diameter, color = 'tab:red')
        else:
            # Updates the threshold value
            self.ys_diameter_zscore = (np.array(self.ys_diameter) - self.thresh[0])/self.thresh[1]
            self.ax.set_ylabel('Eye Diameter (Z-Score)', color='tab:red', labelpad=15)
            self.ax.plot(self.xs, self.ys_diameter_zscore, color = 'tab:red')
            self.ax.axhline(y = self.threshValue, color = 'g', linestyle = '-')
            self.ax.set_ylim([-3, 3])
        self.ax.tick_params(axis='y', labelcolor='tab:red')

        # Updates the Speed Graph
        self.ax2.clear()
        self.ax2.set_ylabel('Speed (cm/s)', color='tab:blue', labelpad=15)
        self.ax2.plot(self.xs, self.ys_speed, color = 'tab:blue')
        self.ax2.tick_params(axis='y', labelcolor='tab:blue')
        self.ax2.yaxis.set_label_position("right")
        self.ax2.yaxis.tick_right()
        
        # Finishing touch ups on the graph
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)
        plt.title('Size of Pupil Over Time')
        plt.tight_layout()


    """
    Multiprocessing Function to Plot the graph in real time
    Input: Multiprocessing Value variables of diameter, speed, and threshold
    Output: None
    """
    def plot(self, diameter, speed, thresh, config):

        # Updates the variables with the Multiprocessing Value Object
        self.diameter = diameter
        self.speed = speed
        self.thresh = thresh
        self.threshValue = config["EYE_THRESHOLD"]

        # Plots the graph in real time
        ani = animation.FuncAnimation(self.fig, self.animate, interval=250, cache_frame_data=False)
        plt.show()