from dlclive import Processor
import Graph
import math

class PupilProcessor(Processor):
    def __init__(self, **kwargs):
        super().__init__()
        self.diameter = 0

    def process(self, pose, **kwargs):
        
        # 0 centre
        # 1 top
        # 2 bottom
        # 3 left
        # 4 right
        # 5 topleft
        # 6 topright
        # 7 bottomleft
        # 8 bottomright
        # 9 ref1
        # 10 ref2

        # IF CENTER IS NOT FOUND
        if pose[0, 2] < 0.5:
            self.diameter = 0
            return pose

        centerX = round(pose[0, 0])
        centerY = round(pose[0, 1])
        radiusSum = 0
        activePos = 0

        for i in range(1, 9):
            if pose[i, 2] > 0.8:
                x_ = round(pose[i, 0])
                y_ = round(pose[i, 1])
                radius = math.sqrt((x_ - centerX)**2 + (y_ - centerY)**2)
                radiusSum += radius
                activePos += 1
        
        if activePos == 0:
            return pose
        
        referencePixel = math.sqrt((pose[9, 0] - pose[10,0])**2 + (pose[9, 1] - pose[10, 1])**2)
        ratio = 1.8/referencePixel

        self.diameter = (radiusSum/activePos)*2*ratio
        
        return pose

    def getDiamater(self):
        return self.diameter

    def save(self, filename):
        return 0