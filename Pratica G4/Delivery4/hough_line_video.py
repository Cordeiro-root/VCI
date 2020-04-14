import cv2 as cv
import numpy as np

cap = cv.VideoCapture('robocup.mp4')

while cap.isOpened():
	ret, frame = cap.read()
    	
	if not ret:
        	print("Can't receive frame (stream end?). Exiting ...")
        	break
	
	gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
	edges = cv.Canny(gray,100,200,apertureSize = 3)
	lines = cv.HoughLines(edges,1,np.pi/180,200)

	for line in lines:
	    rho,theta = line[0]
	    a = np.cos(theta)
	    b = np.sin(theta)
	    x0 = a*rho
	    y0 = b*rho
	    x1 = int(x0 + 1000*(-b))
	    y1 = int(y0 + 1000*(a))
	    x2 = int(x0 - 1000*(-b))
	    y2 = int(y0 - 1000*(a))
	    cv.line(frame,(x1,y1),(x2,y2),(0,0,255),2)

	cv.imshow('canny', edges)
	cv.imshow('img', frame)
	k = cv.waitKey(5) & 0xFF
	if k == 27:
		break

cap.release()
cv.destroyAllWindows()
