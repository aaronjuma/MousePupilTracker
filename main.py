import PupilTracker.GUI as GUI
import MouseTracker as MouseTracker
import multiprocessing

if __name__ == '__main__':
    multiprocessing.freeze_support()
    gui = GUI.GUI()
    gui.start()
    p = multiprocessing.Process(target= MouseTracker.main)
    p.start()
    p.join()
    