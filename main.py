import sys
import os
import PupilProcessor
import Webcam as Webcam
import keyboard
import SerialRecorder
import Logger
import Graph
import multiprocessing
from dlclive import DLCLive

# CONFIG VARIABLES
LOGGER_STATUS = False
GRAPH_STATUS = True

ARDUINO_STATUS = False

def main():
    # Camera Setup
    cam = Webcam.Webcam()
    if cam.start() == False:
        print("Camera Error")
        return False
    
    # DeepLabCut Setup
    dlc_proc = PupilProcessor.PupilProcessor()
    model_path = os.getcwd() + '/DLC_Mice_resnet_50_iteration-1_shuffle-1/'
    dlc_live = DLCLive(model_path, processor = dlc_proc, display = True, display_radius = 2, resize = 1)
    dlc_live.init_inference(cam.getFrame())

    # Logging Setup
    if LOGGER_STATUS:
        logger = Logger.Logger()
        logger.initialize('log1.csv')
    
    # Graphing Setup
    if GRAPH_STATUS:
        graph = Graph.Graph()
        d = multiprocessing.Value('d', 0.0)
        p = multiprocessing.Process(target=graph.plot, args=(d,))
        p.start()
        
    # Arduino Setup
    if ARDUINO_STATUS:
        arduino = SerialRecorder.SerialRecorder()
        if arduino.status() == False:
            print("Unable to find arduino")
            return False
        arduino.run()

    print("Press 'enter' to exit the program...")
    # Runs the program
    while(True):
        frame = cam.getFrame()
        dlc_live.get_pose(frame)
        dia = dlc_proc.getDiamater()
        
        if LOGGER_STATUS: logger.update(dia)
        if GRAPH_STATUS: d.value = dia
        if ARDUINO_STATUS: arduino.update(dia)

        #Leave the program, press enter
        if keyboard.is_pressed('ENTER'):
            break                   

    # Ends the program
    if GRAPH_STATUS: p.terminate()
    if LOGGER_STATUS: logger.stop()
    if ARDUINO_STATUS: arduino.stop()
    cam.close()
    print("Exiting program...")
    return True
    
    
    

if __name__ == '__main__':
    if main():
        sys.exit(0)
    else:
        sys.exit(1)