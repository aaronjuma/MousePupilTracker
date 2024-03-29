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

    # Loads the config file containing the parameters
    with open("Data/config.yaml", "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    # Sets up the camera and ends program if no camera is found
    cam = Webcam.Webcam()
    if cam.start() == False:
        print("Camera Error")
        return False
    
    # Sets up the arduino and ends program if no arduino is found
    arduino = Arduino.Arduino()
    if arduino.status() == False:
        print("Unable to find arduino")
        return False
    arduino.start()
    controller = Controller.Controller(arduino, config)
    
    # DeepLabCut Setup
    dlc_proc = PupilProcessor.PupilProcessor()
    model_path = os.getcwd() + "/PupilTracker/DLC_Mice_resnet_50_iteration-1_shuffle-1/"
    dlc_live = DLCLive(model_path, processor = dlc_proc, display = True, display_radius = 2, resize = 1)
    dlc_live.init_inference(cam.getFrame())

    # Logging Setup
    logger = Logger.Logger()
    
    # Graphing Setup
    graph = Graph.Graph(config)
    graph_diameter = multiprocessing.Value('d', 0.0)
    graph_speed = multiprocessing.Value('d', 0.0)
    graph_thresh = multiprocessing.Array('d', [float("nan"), float("nan")])
    p = multiprocessing.Process(target=graph.plot, args=(graph_diameter, graph_speed, graph_thresh, config))
    p.start()


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
        

        # Initialize the Sampling Period
        if mode == 0:
            print("RECORDING PERIOD")
            logger.start()
            logger.setType("SAMPLE")
            mode = 1

        # The loop code for Sampling Period
        elif mode == 1:
            if (time.time() - startTime) > float(config["SAMPLE_DURATION"]):
                mode = 2
            else:
                logger.update(pupil = dia)

        # Initialize the Trial Period
        elif mode == 2:
            print("TRIAL PERIOD")
            logger.setType("TRIAL")

            # Controller updates threshold
            threshMean, threshSTD = TC.getThresholdParams(logger.getDirec())
            controller.start(threshMean, threshSTD)
            print(threshMean)
            print(threshSTD)
            graph_thresh[0] = threshMean
            graph_thresh[1] = threshSTD
            startTime = time.time()
            mode = 3

        # The loop code for the Trial Period
        elif mode == 3:
            if (time.time() - startTime) > float(config["TRIAL_DURATION"]):
                print("FINISHED")
                break
            else:
                logger.update(pupil=dia, speed=arduino.getBin(), sysStatus=controller.getStatus())
                controller.updateValues(dia, spe)
        
        # Updates the graph about the diameter and speed
        graph_diameter.value, graph_speed.value = dia, spe


    # Ends the program
    dlc_live.close()
    p.terminate()
    logger.stop()
    arduino.stop()
    controller.stop()
    cam.close()
    print("Exiting program...")
    return True