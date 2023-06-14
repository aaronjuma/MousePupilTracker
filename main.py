
# import the opencv library
import cv2
import sys
import os
import PongProcessor
import Cameras.Webcam as Webcam
import Cameras.FLIRCamera as FLIRCamera
import keyboard
import SerialRecorder
import Logger
from dlclive import DLCLive

def main():
    # arduino = SerialRecorder.SerialRecorder()
    cam = Webcam.Webcam()
    
    # if arduino.status() == False:
    #     print("Unable to find arduino")
    #     return False
    
    if cam.start() == False:
        print("Camera Error")
        return False
    
    dlc_proc = PongProcessor.PongProcessor()
    model_path = os.getcwd() + '/DLC_Ping_resnet_50_iteration-1_shuffle-1/'
    dlc_live = DLCLive(model_path, processor = dlc_proc, display = True, display_radius = 6, resize = 0.50)
    dlc_live.init_inference(cam.getFrame())

    logger = Logger.Logger()
    logger.initialize('log1.csv')

    while(True):
        frame = cam.getFrame()
        dlc_live.get_pose(frame)
        logger.update(dlc_proc.getDiamater())

        #Leave the program, press enter
        if keyboard.is_pressed('ENTER'):
            break                   

    logger.stop()
    cam.close()
    print("Exiting program...")
    return True
    
    
if __name__ == '__main__':
    if main():
        sys.exit(0)
    else:
        sys.exit(1)