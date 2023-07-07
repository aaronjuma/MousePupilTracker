from dlclive import Processor
import Graph
import math

class PupilProcessor(Processor):
    def __init__(self, **kwargs):
        super().__init__()
        self.diameter = 0

    def process(self, pose, **kwargs):
        
        # 0 top
        # 1 bottom
        # 2 left
        # 3 right
        # 4 topleft
        # 5 topright
        # 6 bottomleft
        # 7 bottomright
        # 8 center

        # IF CENTER IS NOT FOUND
        if pose[8, 2] < 0.5:
            self.diameter = 0
            return pose

        centerX = round(pose[8, 0])
        centerY = round(pose[8, 1])
        radiusSum = 0
        activePos = 0

        for i in range(0, 8):
            if pose[i, 2] > 0.8:
                x_ = round(pose[i, 0])
                y_ = round(pose[i, 1])
                radius = math.sqrt((x_ - centerX)**2 + (y_ - centerY)**2)
                radiusSum += radius
                activePos += 1
        
        if activePos == 0:
            return pose
        
        self.diameter = (radiusSum/activePos)*2
        
        return pose

    def getDiamater(self):
        return self.diameter

    def save(self, filename):
        return 0