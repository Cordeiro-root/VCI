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
    
    imagray=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    imayuv=cv.cvtColor(frame,cv.COLOR_BGR2YUV)
    imahsv=cv.cvtColor(frame,cv.COLOR_BGR2HSV)

    # Display the resulting frame
    cv.imshow('Normal',frame)
    cv.imshow('GRAY', imagray)
    cv.imshow('YUV', imayuv)
    cv.imshow('HSV',imahsv)
    
    #plt.subplot(221), plt.imshow('frame',frame)
    #plt.subplot(222), plt.imshow('imagray',imagray)
    #plt.subplot(223), plt.imshow('imayuv',imayuv)
    #plt.subplot(224), plt.imshow('imahsv',imahsv)	
    #plt.show()
    
    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
