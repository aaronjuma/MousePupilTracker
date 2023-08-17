import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Graph:
    def __init__(self, config):
        # plt.ion()
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax2 = self.ax.twinx()
        self.xs = []
        self.ys_speed = []
        self.ys_diameter = []
        self.diameter = 0
        self.speed = 0
        self.config = config
        # self.thresh = config["Mice"]["Mouse"+str(config["Mouse"])]["MEAN"]+config["Mice"]["Mouse"+str(config["Mouse"])]["STD"]
        self.start_time = time.time()
        
    def animate(self, i):
        self.xs.append(round(time.time() - self.start_time, 1))
        self.ys_diameter.append(self.diameter.value)
        self.ys_speed.append(self.speed.value)
        
        self.xs = self.xs[-100:]
        self.ys_diameter = self.ys_diameter[-100:]
        self.ys_speed = self.ys_speed[-100:]

        self.ax.clear()
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Eye Diameter (mm)', color='tab:red')
        self.ax.plot(self.xs, self.ys_diameter, color = 'tab:red')
        self.ax.tick_params(axis='y', labelcolor='tab:red')
        # self.ax.axhline(y = self.thresh, color = 'g', linestyle = '-')

        # self.ax2.clear()
        self.ax2.set_ylabel('Speed (pixels)', color='tab:blue')
        self.ax2.plot(self.xs, self.ys_speed, color = 'tab:blue')
        self.ax2.tick_params(axis='y', labelcolor='tab:blue')
        
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)
        plt.title('Size of Pupil Over Time')
        
    def plot(self, diameter, speed):
        self.diameter = diameter
        self.speed = speed
        ani = animation.FuncAnimation(self.fig, self.animate, interval=500, cache_frame_data=False)
        plt.show()