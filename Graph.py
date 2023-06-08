import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Graph:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.xs = []
        self.ys = []
        self.data = 0
        self.start_time = time.time()
        
    def update(self, num):
        self.data = num
        
    def animate(self, i, xs, ys):
        self.xs.append(round(time.time() - self.start_time))
        self.ys.append(self.data)

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
        
    def initGraph(self):
        self.ani = animation.FuncAnimation(self.fig, self.animate, fargs=(self.xs, self.ys), interval=1000)
        plt.show()