import GUI as GUI
import MouseTracker as MouseTracker
import multiprocessing

if __name__ == '__main__':
    multiprocessing.freeze_support()
    gui = GUI.GUI()
    gui.start()
    # d = multiprocessing.Process(target= GUI.start)
    p = multiprocessing.Process(target= MouseTracker.main)
    # d.start()
    p.start()
    # d.join()
    p.join()
    