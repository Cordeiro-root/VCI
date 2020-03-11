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
    
    gauss = cv.GaussianBlur(frame,(15,15),0)
    median = cv.medianBlur(frame,5)
    bilateral = cv.bilateralFilter(frame,9,75,75)
    
    # Display the resulting frames

    cv.imshow('Normal',frame)
    cv.imshow('GaussianBlur',gauss)
    cv.imshow('MedianBlur',median)
    cv.imshow('BilateralBlur',bilateral)
    
    if cv.waitKey(5) == ord('q'):
        break
# When everything done, release the capture 
 
cap.release()
cv.destroyAllWindows()
