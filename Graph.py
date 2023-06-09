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
        self.start_time = time.time()
        
    def animate(self, num):
        self.xs.append(round(time.time() - self.start_time))
        self.ys.append(num)

        # Limit x and y lists to 20 items
        self.xs = self.xs[-20:]
        self.ys = self.ys[-20:]
        
        self.ax.clear()
        self.ax.plot(self.xs, self.ys)
        
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)
        plt.title('Size of Circle Over Time')
        plt.ylabel('Size (pixels)')
        plt.xlabel('Time')
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()