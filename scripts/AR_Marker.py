# -*- coding: utf-8 -*-
"""
Last Updated on October 8 2019

@author: Thomas Talasco
"""

class AR_Marker:
    def calculate_midpoint(self, points):
        return (points[0] + points[1])/2
        
    def __init__(self, corners, id_num):
        self.corners = corners
        Xcords = (corners[0][0][0][0], corners[0][0][2][0])
        Ycords = (corners[0][0][0][1], corners[0][0][2][1])
        self.center = (self.calculate_midpoint(Xcords), self.calculate_midpoint(Ycords))
        self.id_num = id_num
        self.z= 0
        self.angular = 0
        self.x = self.center[0]
        self.y = self.center[1]