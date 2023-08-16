import GUI
import main
import multiprocessing

if __name__ == '__main__':
    multiprocessing.freeze_support()
    gui = GUI.GUI()
    gui.start()
    # d = multiprocessing.Process(target= GUI.start)
    p = multiprocessing.Process(target= main.main)
    # d.start()
    p.start()
    # d.join()
    p.join()
    