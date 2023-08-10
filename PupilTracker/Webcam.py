import cv2

class Webcam:
    
    def __init__(self):
        self.cam = None
    
    def start(self):
        print("Setting up camera..")
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
        grabbed, frame = self.cam.read()
        if not self.cam.isOpened():
            return False
        return True
               
    def close(self):
        self.cam.release()
        
    def getFrame(self):
        ret, frame = self.cam.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # frame = cv2.rotate(frame, cv2.ROTATE_180)
        return frame
