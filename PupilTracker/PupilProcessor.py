from dlclive import Processor
import PupilTracker.Graph as Graph
import math

class PupilProcessor(Processor):
    def __init__(self, **kwargs):
        super().__init__()
        self.diameter = 0

    def process(self, pose, **kwargs):
        
        # 0. centre
        # 1. top
        # 2. bottom
        # 3. left
        # 4. right
        # 5. topleft
        # 6. topright
        # 7. bottomleft
        # 8. bottomright

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

        self.diameter = round((radiusSum/activePos)*2, 2)
        
        return pose

    def getDiamater(self):
        return self.diameter

    def save(self, filename):
        return 0