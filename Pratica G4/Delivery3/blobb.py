#!/usr/bin/python

# Standard imports
import cv2
import numpy as np

# Read image
im = cv2.imread("ball.png")
hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
# define range of blue color in HSV
lower_yellow = np.array([21,40,0])
upper_yellow = np.array([51,255,255])
masky = cv2.inRange(hsv, lower_yellow, upper_yellow)
resy = cv2.bitwise_and(im,im, mask= masky)
imgray=cv2.cvtColor(resy,cv2.COLOR_BGR2GRAY)

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
#params.minThreshold = 10
#params.maxThreshold = 200

#Filter by color
params.filterByColor=1
params.blobColor=255

# Filter by Area.
#params.filterByArea = True
#params.minArea = 1500

# Filter by Circularity
#params.filterByCircularity = True
#params.minCircularity = 0.1
#params.maxCircularity = 1

# Filter by Convexity
#params.filterByConvexity = True
#params.minConvexity = 0.87
    
# Filter by Inertia
#params.filterByInertia = True
#params.minInertiaRatio =0.01
#params.maxInertiaRatio =1

# Create a detector with the parameters
ver = (cv2.__version__).split('.')
if int(ver[0]) < 3 :
	detector = cv2.SimpleBlobDetector(params)
else : 
	detector = cv2.SimpleBlobDetector_create(params)


# Detect blobs.
keypoints = detector.detect(imgray)

# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
# the size of the circle corresponds to the size of blob

im_with_keypoints = cv2.drawKeypoints(imgray, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Show blobs
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)
cv2.destroyAllWindows()
