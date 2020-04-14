import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

def event(value):
    pass

cap = cv.VideoCapture('robocup.mp4')

cv.namedWindow('Threshold')
cv.createTrackbar('Threshold1','Threshold',0,250,event)
cv.createTrackbar('Threshold2','Threshold',0,250,event)

while cap.isOpened():
	ret, frame = cap.read()
    	
	if not ret:
        	print("Can't receive frame (stream end?). Exiting ...")
        	break
	
	threshold1 = cv.getTrackbarPos('Threshold1','Threshold')
    	threshold2 = cv.getTrackbarPos('Threshold2','Threshold')
	edges = cv.Canny(frame,threshold1,threshold2)
	
	cv.imshow('Original video', frame)
	cv.imshow('Edges',edges)

	k = cv.waitKey(5) & 0xFF
	if k == 27:
		break
cap.release()
cv.destroyAllWindows()
