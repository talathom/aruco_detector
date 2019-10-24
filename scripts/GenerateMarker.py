#!/usr/bin/env python
"""
Last Updated on October 7 2019

@author: Thomas Talasco
"""

import sys
import cv2
from cv2 import aruco

PIXELS_PER_INCH = 96
ARG_LENGTH = 3 # Required number of arguments no more, no less
MARKER_ID_UPPER_BOUND = 249 #Highest ID in AR dict
MARKER_ID_LOWER_BOUND = 0 # Lowest ID in AR dict
MIN_PIXELS = 6 # Minimum number of pixels is 6 since we're using a 6x6 Dictionary

#Import AR Dictionary
ar_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
#Verify correct num of args
if len(sys.argv) != ARG_LENGTH:
    print("Invalid args - Usage: marker_id sidelengthinches")
else:
    #Verify correct format
    try:
        marker_id = int(sys.argv[1])
        if marker_id > MARKER_ID_UPPER_BOUND or marker_id < MARKER_ID_LOWER_BOUND:
            sys.exit(1) #Throw exception on bad ID
    except:
        print("Invalid Marker ID, Valid ID 0-249")
    try:
        inches = int(sys.argv[2])
    except:
        print("Inches arg must be an integer")
    marker_size = inches * PIXELS_PER_INCH # Get size in pixels
    if marker_size < MIN_PIXELS:
        print("Cannot create 6x6 Marker with a size of 5x5 or smaller")
    else:
        #Write to file
        ar_marker = aruco.drawMarker(ar_dict, marker_id, marker_size)
        cv2.imwrite('ar'+ str(marker_id) +'.png', ar_marker)