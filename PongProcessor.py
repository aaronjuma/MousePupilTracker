from dlclive import Processor
import time
import math

class PongProcessor(Processor):
    def __init__(self, **kwargs):
        super().__init__()

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
            horzDis = abs(left[1]-right[1])
        else:
            horzDis = None
            
        diam = -1
        if horzDis == None and vertDis == None:
            diam = None
        elif horzDis == None:
            diam = vertDis
        elif vertDis == None:
            diam = horzDis
        else:
            diam = (vertDis+horzDis)/2
        print(diam)
        
        return pose

    def save(self, filename):
        return 0