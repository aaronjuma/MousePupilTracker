import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Graph:
    def __init__(self):
        plt.ion()
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.xs = []
        self.ys = []
        self.data = 0
        self.start_time = time.time()
        
    def animate(self, i):
        self.xs.append(round(time.time() - self.start_time, 1))
        self.ys.append(self.data.value)
        self.xs = self.xs[-100:]
        self.ys = self.ys[-100:]
        self.ax.clear()
        self.ax.plot(self.xs, self.ys)
        
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)
        plt.title('Size of Circle Over Time')
        plt.ylabel('Size (mm)')
        plt.xlabel('Time')
        
    def plot(self, data):
        self.data = data
        print("Beginning Plot...")
        ani = animation.FuncAnimation(self.fig, self.animate, interval=500, cache_frame_data=False)
        plt.show()