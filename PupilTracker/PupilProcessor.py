"""
PupilProcessor.py
This class is responsible for doing the pupil diameter calculations by
getting the data directly from DeepLabCut and using the points to calculate
the diameter.
"""

from dlclive import Processor
import math

class PupilProcessor(Processor):

    """
    Initializer for the PupilProcessor Class
    Input: None
    Output: None
    """
    def __init__(self, **kwargs):
        super().__init__()
        self.diameter = 0


    """
    Processes the data points from DeepLabCut
    Input: None
    Output: None
    """
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

        # If the center is not found, it will return 0
        if pose[0, 2] < 0.5:
            self.diameter = 0
            return pose

        # Gets the center point coordinate
        centerX = round(pose[0, 0])
        centerY = round(pose[0, 1])

        # Set up for diameter calculations
        radiusSum = 0
        activePos = 0

        # Loops through all the data points
        for i in range(1, 9):

            # Checks for data points that are confident (they are for sure data points)
            if pose[i, 2] > 0.8:

                # Gets the current data point's coordinates
                x_ = round(pose[i, 0])
                y_ = round(pose[i, 1])

                # Calculates its distance from the centre point (radius)
                radius = math.sqrt((x_ - centerX)**2 + (y_ - centerY)**2)

                # Adds it onto current sum
                radiusSum += radius
                activePos += 1
        
        # Just in case so it does not divide by 0
        if activePos == 0:
            return pose

        # Calculates the diameter by averaging the radius values, and multiplying by 2
        # Diameter = (Average Radius)*2
        self.diameter = round((radiusSum/activePos)*2, 2)
        
        return pose


    """
    Used by the main program to recieve the diameter value
    Input: None
    Output: None
    """
    def getDiamater(self):
        return self.diameter

    def save(self, filename):
        return 0