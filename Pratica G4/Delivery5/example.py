# Implement an algorithm to perform multi-object tracking. Start by using the 
# developed object detection algorithms during the previous deliverables and 
# implement a solution that should be able to distinguish which objects are 
# being tracked (multiple balls and robots; assigning an unique ID to each 
# one,  etc)

import numpy as np
import cv2 as cv

def event(value):
    pass

cap = cv.VideoCapture('video.mp4')

cv.namedWindow('Object tracking')

while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    frame = cv.resize(frame, (1080, 700))
    
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
    # 0) cv.bilateralFilter() is highly effective in noise removal while 
    #    keeping edges sharp. Better results, but it takes a lot of time!
    #frame = cv.bilateralFilter(imgray, 10, 75, 75)
    
    # 1) Contour detection (Robots)
    low = np.array([80, 80, 80])
    high = np.array([95, 195, 195])
    mask = cv.inRange(hsv, low, high)
    res = cv.bitwise_and(frame, frame, mask = mask)
    res = cv.cvtColor(res, cv.COLOR_BGR2GRAY)
    
    contours_robots, hierarchy = cv.findContours(res, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    # 2) Contour detection (Balls)
    low = np.array([0, 93, 52])
    high = np.array([40, 236, 255])
    mask = cv.inRange(hsv, low, high)
    res = cv.bitwise_and(frame, frame, mask = mask)
    res = cv.cvtColor(res, cv.COLOR_BGR2GRAY)
    
    contours_balls, hierarchy = cv.findContours(res, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    # 3) Draw balls
    cv.drawContours(frame, contours_robots, -1, (0, 0, 255), 2)
    cv.drawContours(frame, contours_balls, -1, (255, 0, 0), 2)
    cv.imshow('Object tracking', frame)
    

    k = cv.waitKey(25) & 0xFF
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()