
# import the opencv library
import cv2
import os
import PySpin
import FLIRCamera
from dlclive import DLCLive, Processor
  
cam = FLIRCamera.FLIRCamera()
dlc_proc = Processor()

model_path = os.getcwd() + '/DLC_Ping_resnet_50_iteration-0_shuffle-1-lite/'
dlc_live = DLCLive(model_path, processor = dlc_proc, display = True, display_radius = 6, resize = 0.35)
dlc_live.init_inference(cam.getFrame())
cam.releaseFrame()

while(True):
    frame = cam.getFrame()
    # Display the resulting frame
    cv2.imshow('frame', frame)
    dlc_live.get_pose(frame)
    cam.releaseFrame()
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.close()
# Destroy all the windows
cv2.destroyAllWindows()