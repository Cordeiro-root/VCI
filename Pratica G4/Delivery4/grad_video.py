import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

def event(value):
    pass

cap = cv.VideoCapture('robocup.mp4')

while cap.isOpened():
	ret, frame = cap.read()
	frameg = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    	
	if not ret:
		print("Can't receive frame (stream end?). Exiting ...")
		break
	laplacian = cv.Laplacian(frameg,cv.CV_64F)
	#sobelx = cv.Sobel(frame,cv.CV_64F,1,0,ksize=5)
	#sobely = cv.Sobel(frame,cv.CV_64F,0,1,ksize=-1)
	#scharr = cv.Scharr(frameg,cv.CV_64F,0,1)
	
	cv.imshow('Original video', frame)
	cv.imshow('laplacian',laplacian)

	k = cv.waitKey(5) & 0xFF
	if k == 27:
		break
cap.release()
cv.destroyAllWindows()