import sys
import os
import time
import PupilTracker.PupilProcessor as PupilProcessor
import PupilTracker.Webcam as Webcam
import keyboard
import PupilTracker.Arduino as Arduino
import PupilTracker.Logger as Logger
import PupilTracker.Graph as Graph
import PupilTracker.Controller as Controller
import PupilTracker.ThresholdCalculator as TC
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
    
    # Graphing Setup
    if config["grapher"]:
        graph = Graph.Graph(config)
        graph_diameter = multiprocessing.Value('d', 0.0)
        graph_speed = multiprocessing.Value('d', 0.0)
        graph_thresh = multiprocessing.Value('d', 0.0)
        p = multiprocessing.Process(target=graph.plot, args=(graph_diameter, graph_speed))
        p.start()
        
    # Arduino Setup
    if config["arduino"]:
        arduino = Arduino.Arduino()
        if arduino.status() == False:
            print("Unable to find arduino")
            return False
        arduino.start()
        controller = Controller.Controller(arduino, config)

    '''
    Mode 0 = Sample Init
    Mode 1 = Sample
    Mode 2 = Trial Init
    Mode 3 = Trial
    '''
    mode = 0
    startTime = time.time()

    print("Press 'escape' to exit the program...")
    # Runs the program
    while(True):

        #Leave the program, press escape
        if keyboard.is_pressed('ESC'):
            break    

        # Basic Frame Calculations
        frame = cam.getFrame()
        dlc_live.get_pose(frame)
        dia = dlc_proc.getDiamater()
        spe = arduino.getValue()

        if mode == 0:
            print("RECORDING PERIOD")
            logger.initialize()
            logger.setType("SAMPLE")
            mode = 1
        elif mode == 1:
            if (time.time() - startTime) > 300:
                mode = 2
            else:
                logger.update(pupil = dia)
        elif mode == 2:
            print("TRIAL PERIOD")
            logger.setType("TRIAL")
            # Controller updates threshold
            calc = TC.ThresholdCalculator(logger.getDirec())
            calc.run()
            controller.start(calc.getMean(), calc.getSTD())
            print(calc.getMean())
            print(calc.getSTD())
            mode = 3
        elif mode == 3:
            logger.update(pupil=dia, speed=arduino.getBin(), sysStatus=controller.getStatus())
            controller.updateValues(dia, spe)
        
        graph_diameter.value, graph_speed.value  = dia, spe      

    # Ends the program
    if config["grapher"]: p.terminate()
    if config["logger"]: logger.stop()
    if config["arduino"]: arduino.stop()
    controller.stop()
    cam.close()
    print("Exiting program...")
    return True

if __name__ == '__main__':
    if main():
        sys.exit(0)
    else:
        sys.exit(1)