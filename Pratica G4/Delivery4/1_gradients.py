import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

def event(value):
    pass

cap = cv.VideoCapture('robocup.mp4')

cv.namedWindow('0: Laplacian, 1: SobelX, 2: SobelY, 3: Scharr')

cv.createTrackbar('ID', '0: Laplacian, 1: SobelX, 2: SobelY, 3: Scharr', 0, 3, event)

while cap.isOpened():
    ret, frame = cap.read()
    frameg = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    id = cv.getTrackbarPos('ID', '0: Laplacian, 1: SobelX, 2: SobelY, 3: Scharr')
    
    res = None;
    
    if(id == 0):
        res = cv.Laplacian(frameg,cv.CV_64F)
    if(id == 1):
        res = cv.Sobel(frame,cv.CV_64F,1,0,ksize=5)
    if(id == 2):
        res = cv.Sobel(frame,cv.CV_64F,0,1,ksize=-1)
    if(id == 3):
        res = cv.Scharr(frameg,cv.CV_64F,0,1)
	
	#cv.imshow('Original video', frame)
    cv.imshow('0: Laplacian, 1: SobelX, 2: SobelY, 3: Scharr', res)
    
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
    
cap.release()
cv.destroyAllWindows()