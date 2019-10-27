#!/usr/bin/env python
"""
Last Updated on October 27 2019

@author: Thomas Talasco
"""

from cv2 import aruco
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
from aruco_detector.msg import ArucoMessage
from AR_Marker import AR_Marker
import math
    
message = ArucoMessage()
METERS_PER_FEET = 3.281

class Aruco_Detector:
    def __init__(self):
        self.bridge = CvBridge()
        self.ar_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        self.param = aruco.DetectorParameters_create()
        self.markers = list()
        self.image_sub = rospy.Subscriber("/camera/rgb/image_color", Image, self.image_callback)
        self.depth_sub = rospy.Subscriber("/camera/depth/image", Image, self.depth_callback)
        # Topic for publishing AR messages
        self.pub = rospy.Publisher("/aruco_detector/ArucoMessage", ArucoMessage, queue_size=10)
        #Length and Width of image
        self.img_y = 0
        self.img_x = 0 
        #Center of the image coordinates
        self.img_center_y = 0
        self.img_center_x = 0
        self.depth_image = [[0 for x in range(640)] for y in range(480)] # initialize zero array
        rospy.spin()
        
    def depth_callback(self, data):
        try:
            self.depth_image = np.asarray(self.bridge.imgmsg_to_cv2(data, '32FC1'))
            # Build a cv_image from the data in the depth image callback
        except CvBridgeError as e:
            print(e)
            
    def image_callback(self, data):
        try:
            cv_image = np.asarray(self.bridge.imgmsg_to_cv2(data, "bgr8"))
            #build a color image and check for AR markers in it
        except CvBridgeError as e:
            print(e)
            
        # Get image height and width
        img_shape = cv_image.shape
        self.img_y = img_shape[0] #Image length
        self.img_x = img_shape[1] #Image width
        
        #Find Image midpoint
        self.img_center_y = self.img_y/2
        self.img_center_x = self.img_x/2
        
        # Detect markers using OpenCV library        
        corners, ids, rejectedImgPoints = aruco.detectMarkers(cv_image, self.ar_dict, parameters=self.param)
        for i in range(0, len(corners)):
            # Build list of marker objects for each detected marker
            new_marker = AR_Marker(corners, int(ids[i]))
            self.markers.append(new_marker)
            
        for marker in self.markers:
            marker.z = self.depth_image[int(marker.y)][int(marker.x)]*METERS_PER_FEET #Converts meters to feet
            if math.isnan(marker.z): # Check if marker is too close
                marker.z = -1
                
            #Build message
            message.x = marker.x
            message.y = marker.y
            message.z = marker.z
            message.id = marker.id_num
            
            #Calculate angular coord by finding the angle between the vector which points to the center of the marker and the vector which represents the midpoint of the image
            vector_mult = self.img_center_x*marker.x + self.img_center_y*marker.y
            vector_magnitudes = self.getVectorMagnitude(self.img_center_x, self.img_center_y) * self.getVectorMagnitude(marker.x, marker.y)
            
            # Find the angle between the vectors in degrees
            marker.angular = math.degrees(math.acos(vector_mult / vector_magnitudes))
            # Invert the angle if on left side of image to give it direction
            if marker.x < self.img_center_x:
                marker.angular = -marker.angular
            
            message.angular = marker.angular
            
            # Publish the Message!
            self.pub.publish(message)
        
        #Clear marker list for next callback
        del self.markers[:]
        
    def getVectorMagnitude(self, x, y):
        #Distance formula
        return math.sqrt(pow(x, 2) + pow(y, 2))
            
if __name__ == '__main__':
    rospy.init_node('aruco_detector', anonymous=True)
    aruco_class = Aruco_Detector()
        
        
