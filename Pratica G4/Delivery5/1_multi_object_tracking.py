# Implement an algorithm to perform multi-object tracking. Start by using the 
# developed object detection algorithms during the previous deliverables and 
# implement a solution that should be able to distinguish which objects are 
# being tracked (multiple balls and robots; assigning an unique ID to each 
# one,  etc)

import numpy as np
import cv2 as cv

def event(value):
    pass

cap = cv.VideoCapture('video.mov')

cv.namedWindow('Ball and lines')

while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    imgray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    # 1) Contour detection
    ret, thresh = cv.threshold(imgray, 100, 255, cv.THRESH_TOZERO_INV)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    # 2) Remove wrong contours
    good_contours = []
    
    # 2.1) Keep only contours with more than 50 points
    for k in contours:
        if(k.shape[0] >= 50):
            good_contours.append(k)

    # X) Display the frame   
    cv.drawContours(frame, good_contours, -1, (0,0,255), 3)     
    cv.imshow('Ball and lines', frame)

    k = cv.waitKey(25) & 0xFF
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()
