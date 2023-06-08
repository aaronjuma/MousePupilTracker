
# import the opencv library
import cv2
import os
import PongProcessor
import FLIRCamera
import keyboard
from dlclive import DLCLive, Processor

cam = FLIRCamera.FLIRCamera()

if cam.initialize() == False:
    print("Unable to find camera")
    print("Exiting program...")
    quit()

dlc_proc = PongProcessor.PongProcessor()
model_path = os.getcwd() + '/DLC_Ping_resnet_50_iteration-1_shuffle-1/'
dlc_live = DLCLive(model_path, processor = dlc_proc, display = True, display_radius = 6, resize = 0.75)

dlc_live.init_inference(cam.getFrame())
cam.releaseFrame()

while(True):
    frame = cam.getFrame()
    # Display the resulting frame
    # cv2.imshow('frame', frame)
    dlc_live.get_pose(frame)
    cam.releaseFrame()

    #Leave the program, press enter
    if keyboard.is_pressed('ENTER'):
            break                   

cam.close()
# cv2.destroyAllWindows()
print("Exiting program...")