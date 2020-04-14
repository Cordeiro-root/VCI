import numpy as np
import cv2 as cv

img = cv.imread('robo.png')
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
edges = cv.Canny(gray,50,150,apertureSize = 3)
circles = cv.HoughCircles(edges,cv.HOUGH_GRADIENT,1,200,param1=50,param2=80,minRadius=0,maxRadius=0)
circles = np.uint16(np.around(circles))

for i in circles[0,:]:
    # draw the outer circle
    cv.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv.circle(img,(i[0],i[1]),2,(0,0,255),3)

cv.imshow('detected circles',img)
cv.waitKey(0)
cv.destroyAllWindows()
