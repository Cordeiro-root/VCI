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

	imgray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
	ret, thresh = cv.threshold(imgray, threshold1, threshold2, 0)
	contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	
	cv.imshow('Original video', frame)
	cv.drawContours(frame, contours, -1, (0,0,255), 3)
	cv.imshow('Contours',frame)

	k = cv.waitKey(5) & 0xFF
	if k == 27:
		break
cap.release()
cv.destroyAllWindows()
