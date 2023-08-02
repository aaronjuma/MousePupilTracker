import sys
import os
import PupilTracker.PupilProcessor as PupilProcessor
import PupilTracker.Webcam as Webcam
import keyboard
import PupilTracker.Arduino as Arduino
import PupilTracker.Logger as Logger
import PupilTracker.Graph as Graph
import PupilTracker.Controller as Controller
import multiprocessing
import yaml
from dlclive import DLCLive

def main():

    # Loading Config File
    with open("config.yaml", "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    # Camera Setup
    cam = Webcam.Webcam()
    if cam.start() == False:
        print("Camera Error")
        return False
    
    # DeepLabCut Setup
    dlc_proc = PupilProcessor.PupilProcessor()
    model_path = os.getcwd() + config["model"]
    dlc_live = DLCLive(model_path, processor = dlc_proc, display = True, display_radius = 2, resize = 1)
    dlc_live.init_inference(cam.getFrame())

    # Logging Setup
    if config["logger"]:
        logger = Logger.Logger()
        logger.initialize()
    
    # Graphing Setup
    if config["grapher"]:
        graph = Graph.Graph()
        d = multiprocessing.Value('d', 0.0)
        p = multiprocessing.Process(target=graph.plot, args=(d,))
        p.start()
        
    # Arduino Setup
    if config["arduino"]:
        arduino = Arduino.Arduino()
        if arduino.status() == False:
            print("Unable to find arduino")
            return False
        arduino.run()

    # Runs the controller
    controller = Controller.Controller(arduino)
    controller.start()

    print("Press 'enter' to exit the program...")
    # Runs the program
    while(True):
        frame = cam.getFrame()
        dlc_live.get_pose(frame)
        dia = dlc_proc.getDiamater()
        
        if config["logger"]: logger.update(dia)
        if config["grapher"]: d.value = dia
        controller.updateValues(dia)

        #Leave the program, press escape
        if keyboard.is_pressed('ESC'):
            break                   

    # Ends the program
    if config["grapher"]: p.terminate()
    if config["logger"]: logger.stop()
    controller.stop()
    cam.close()
    print("Exiting program...")
    return True

if __name__ == '__main__':
    if main():
        sys.exit(0)
    else:
        sys.exit(1)