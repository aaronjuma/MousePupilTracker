
# import the opencv library
import cv2
import PySpin
import FLIRCamera
from dlclive import DLCLive, Processor
  
cam = FLIRCamera.FLIRCamera()
dlc_proc = Processor()

while(True):
    frame = cam.getFrame()
    # Display the resulting frame
    cv2.imshow('frame', frame)
    cam.releaseFrame()
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Destroy all the windows
cv2.destroyAllWindows()