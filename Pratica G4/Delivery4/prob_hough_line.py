import cv2 as cv
import numpy as np

cap = cv.VideoCapture('robocup.mp4')

while cap.isOpened():
	ret, frame = cap.read()
    	
	if not ret:
		print("Can't receive frame (stream end?). Exiting ...")
        	break
	
	gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
	edges = cv.Canny(gray,50,150,apertureSize = 3)
	lines = cv.HoughLinesP(edges,1,np.pi/180,100,minLineLength=100,maxLineGap=10)

	for line in lines:
    		x1,y1,x2,y2 = line[0]
    		cv.line(frame,(x1,y1),(x2,y2),(0,255,0),2)

	cv.imshow('canny', edges)
	cv.imshow('Probabilistic Hough transform', frame)
	k = cv.waitKey(5) & 0xFF
	if k == 27:
		break

cap.release()
cv.destroyAllWindows()
