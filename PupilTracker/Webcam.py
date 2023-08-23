"""
Webcam.py
This class is responsible for setting up the webcam and getting
the frames of the webcam.
"""
import cv2

class Webcam:
    
    """
    Initializes the Webcam Class
    Input: None
    Output: None
    """
    def __init__(self):
        self.cam = None
    

    """
    Starts the webcam and sets it up
    Input: None
    Output: None
    """
    def start(self):
        print("Setting up camera..")
        
        # Changing Camera Parameters
        self.cam = cv2.VideoCapture(0)
        self.cam.set(cv2.CAP_PROP_FPS, 30)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.cam.set(cv2.CAP_PROP_BRIGHTNESS, 0)
        self.cam.set(cv2.CAP_PROP_CONTRAST, 64)
        self.cam.set(cv2.CAP_PROP_HUE, 0)
        self.cam.set(cv2.CAP_PROP_SATURATION, 60)
        self.cam.set(cv2.CAP_PROP_SHARPNESS, 6)
        self.cam.set(cv2.CAP_PROP_GAMMA, 100)
        self.cam.set(cv2.CAP_PROP_GAIN, 0)
        self.cam.set(cv2.CAP_PROP_EXPOSURE, -6)
        print(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        print(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Loads camera
        grabbed, frame = self.cam.read()

        # If no camera is found, return False to end program
        if not self.cam.isOpened():
            return False
        
        # If camera is found, return True
        return True


    """
    Closes the camera
    Input: None
    Output: None
    """
    def close(self):
        self.cam.release()
        

    """
    Gets the frame of the camera to feed it to DeepLabCut
    Input: None
    Output: Frame
    """
    def getFrame(self):
        ret, frame = self.cam.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # frame = cv2.rotate(frame, cv2.ROTATE_180)
        return frame
