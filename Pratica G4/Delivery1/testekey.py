import numpy as np
import cv2 as cv

img=cv.imread('ml.jpg')
while(1):
    cv.imshow('img',img)
    k = cv.waitKey(33)
    if k==27:    # Esc key to stop
        break
    elif k==-1:  # normally -1 returned,so don't print it
        continue
    else:
        print(k) # else print its value
