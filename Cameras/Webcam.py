import cv2

class Webcam:
    
    def __init__(self):
        self.cam = None
    
    def start(self):
        print("Setting up camera..")
        self.cam = cv2.VideoCapture(0)
        grabbed, frame = self.cam.read()
        if not self.cam.isOpened():
            return False
        return True
               
    def close(self):
        self.cam.release()
        
    def getFrame(self):
        ret, frame = self.cam.read()
        frame = cv2.resize(frame, (640, 512))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return frame
