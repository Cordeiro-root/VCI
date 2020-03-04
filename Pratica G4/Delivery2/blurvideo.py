import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
        
    # Our operations on the frame come here
        
    frame = cv.flip(frame, 1)
    
    #imagray=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    #imayuv=cv.cvtColor(frame,cv.COLOR_BGR2YUV)
    #imahsv=cv.cvtColor(frame,cv.COLOR_BGR2HSV)
    
    #blurg = cv.GaussianBlur(imagray,(15,15),0)
    gauss = cv.GaussianBlur(frame,(15,15),0)
    median = cv.medianBlur(frame,5)
    bilateral = cv.bilateralFilter(frame,9,75,75)
    
    #cv.imshow('Original',frame)
    #cv.imshow('Averaging',blur)
	
    # Display the resulting frames

    cv.imshow('Normal',frame)
    cv.imshow('GaussianBlur',gauss)
    cv.imshow('MedianBlur',median)
    cv.imshow('BilateralBlur',bilateral)
    #cv.imshow('grayblur',blurg)
    #cv.imshow('GRAY', imagray)
    #cv.imshow('YUV', imayuv)
    #cv.imshow('HSV',imahsv)

    
    if cv.waitKey(5) == ord('q'):
        break
# When everything done, release the capture 
 
cap.release()
cv.destroyAllWindows()
