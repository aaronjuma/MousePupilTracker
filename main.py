
# import the opencv library
import cv2
import sys
import os
import PongProcessor
import FLIRCamera
import keyboard
import SerialRecorder
from dlclive import DLCLive, Processor

def main():
    arduino = SerialRecorder.SerialRecorder()
    cam = FLIRCamera.FLIRCamera()
    
    if arduino.status() == False:
        print("Unable to find arduino")
        return False
    
    if cam.begin() == False:
        print("Camera Error")
        return False
    
    
    dlc_proc = PongProcessor.PongProcessor(board = arduino)
    model_path = os.getcwd() + '/DLC_Ping_resnet_50_iteration-1_shuffle-1/'
    dlc_live = DLCLive(model_path, processor = dlc_proc, display = True, display_radius = 6, resize = 0.75)

    dlc_live.init_inference(cam.getFrame())
    cam.releaseFrame()

    while(True):
        frame = cam.getFrame()
        # Display the resulting frame
        # cv2.imshow('frame', frame)
        dlc_live.get_pose(frame, board=arduino)
        cam.releaseFrame()

        #Leave the program, press enter
        if keyboard.is_pressed('ENTER'):
                break                   

    cam.close()
    # cv2.destroyAllWindows()
    print("Exiting program...")
    return True
    
    
if __name__ == '__main__':
    if main():
        sys.exit(0)
    else:
        sys.exit(1)