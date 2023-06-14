import cv2

class Webcam:
    
    def __init__(self):
        print("Setting up camera..")
        self.cam = None
    
    def start(self):
        self.cam = cv2.VideoCapture(0)
        grabbed, frame = self.cam.read()
        if not self.cam.isOpened():
            return False
        return True
               
    def close(self):
        self.cam.release()
        
    def getFrame(self):
        ret, frame = self.cam.read()
        return frame
