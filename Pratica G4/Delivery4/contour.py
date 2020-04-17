import sys
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt


#def event(value):
#    pass

img = cv.imread('robo.png')
#cv.namedWindow('Threshold')
#cv.createTrackbar('Threshold1','Threshold',0,250,event)
#cv.createTrackbar('Threshold2','Threshold',0,250,event)

#threshold1 = cv.getTrackbarPos('Threshold1','Threshold')
#threshold2 = cv.getTrackbarPos('Threshold2','Threshold')

imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 50, 90, 0)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

cv.imshow('ORIGINAL', img)
cv.drawContours(img, contours, -1, (0,0,255), 3)
#cnt=contours[4]
#cv.drawContours(img,[cnt],0,(0,255,0),3)
cv.imshow('Contours', img) 
k=cv.waitKey(0) & 0xFF

#cv.destroyAllWindows()