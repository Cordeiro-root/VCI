import numpy as np
import cv2 as cv

cap = cv.VideoCapture('robocup2.mp4')

while cap.isOpened():
	ret, frame = cap.read()
	if not ret:
		print("Can't receive frame (stream end?). Exiting ...")
        	break

	gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
	edges = cv.Canny(gray,50,150,apertureSize = 3)
	circles = cv.HoughCircles(edges,cv.HOUGH_GRADIENT,1,400,param1=50,param2=80,minRadius=0,maxRadius=0)
	circles = np.uint16(np.around(circles))

	for i in circles[0,:]:
    		# draw the outer circle
    		cv.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
    		# draw the center of the circle
    		#cv.circle(cframe,(i[0],i[1]),2,(0,0,255),3)

	cv.imshow('Circle Hough transform', frame)
	k = cv.waitKey(5) & 0xFF
	if k == 27:
		break

cap.release()
cv.destroyAllWindows()
