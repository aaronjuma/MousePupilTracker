from dlclive import Processor
import Graph

class PongProcessor(Processor):
    def __init__(self, **kwargs):
        super().__init__()
        self.diameter = 0

    def process(self, pose, **kwargs):
        
        # 0 is top
        # 1 is left
        # 2 is right
        # 3 is bot
        top = [round(n) for n in pose[0]] if pose[0, 2] > 0.8 else None
        left = [round(n) for n in pose[1]] if pose[1, 2] > 0.8 else None
        right = [round(n) for n in pose[2]] if pose[2, 2] > 0.8 else None
        bot = [round(n) for n in pose[3]] if pose[3, 2] > 0.8 else None
            
        vertDis = -1
        horzDis = -1
        
        if top != None and bot != None:
            vertDis = abs(top[1] - bot[1])
        else:
            vertDis = None
            
        if left != None and right != None:
            horzDis = abs(left[0]-right[0])
        else:
            horzDis = None
            
        if horzDis == None and vertDis == None:
            self.diam = 0
        elif horzDis == None:
            self.diam = vertDis
        elif vertDis == None:
            self.diam = horzDis
        else:
            self.diam = (vertDis+horzDis)/2
        
        return pose

    def getDiamater(self):
        return self.diam

    def save(self, filename):
        return 0