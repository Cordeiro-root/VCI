import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

while(1):
    # Take each frame
    _, frame = cap.read()
    
    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
    # define range of blue color in HSV
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])

    # define range of green color in HSV
    lower_green = np.array([50,50,50])
    upper_green = np.array([70,255,255])
           
    # define range of red color in HSV
    lower_red = np.array([0,50,50])
    upper_red = np.array([0,255,255])
    
    # define range of blue color in HSV
    lower_yellow = np.array([20,50,50])
    upper_yellow = np.array([40,250,250])
    
    # define range of white color in HSV
    lower_white = np.array([0,0,50])
    upper_white = np.array([0,0,255])
    
    # Threshold the HSV image to getpyt only blue colors
    maskb = cv.inRange(hsv, lower_blue, upper_blue)
    maskg = cv.inRange(hsv, lower_green, upper_green)
    maskr = cv.inRange(hsv, lower_red, upper_red)
    masky = cv.inRange(hsv, lower_yellow, upper_yellow)
    maskw = cv.inRange(hsv, lower_white, upper_white)
    
    
    # Bitwise-AND mask and original image
    resb = cv.bitwise_and(frame,frame, mask= maskb)
    resg = cv.bitwise_and(frame,frame, mask= maskg)
    resr = cv.bitwise_and(frame,frame, mask= maskr)
    resy = cv.bitwise_and(frame,frame, mask= masky)
    resw = cv.bitwise_and(frame,frame, mask= maskw)
    
    
    cv.imshow('frame',frame)
   # cv.imshow('mask',mask)
    cv.imshow('resb',resb)
    cv.imshow('resy',resy)
    cv.imshow('resr',resr)
    cv.imshow('resg',resg)
    cv.imshow('resw',resw)
    
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
        
cv.destroyAllWindows()
