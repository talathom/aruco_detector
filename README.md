# Overview
Detects Aruco Markers and returns their XYZ coordinates within a 2D OpenCV Image as well as the Marker's ID within the 6x6 aruco dictionary and the markers angular value relative to the center of the image

# Generate Marker
Usage run GenerateMarker.py with exactly two args. The first being the ID number of the marker you wish to generate, the second being the length of a side of the marker (Markers are squares so all sides are the same length).

Example: python GenerateMarker.py 0 3
This generates marker ID 0 3x3 inches in size and saves it to the working directory ar0.png

# Aruco_Detector.py
To begin detecting AR Markers you must first launch openni.launch and then launch the Aruco_Detector.py script this can be done by executing rosrun aruco_detector Aruco_Detector.py which will then begin publishing messages on /aruco_detector/ArucoMessage
