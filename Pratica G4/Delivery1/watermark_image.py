import numpy as np
import cv2 as cv

#img1 over img2
img1 = cv.imread('frame1.png')
img2 = cv.imread('frame.png')

dst = cv.addWeighted(img1,0.7,img2,0.3,0)


cv.imshow('dst',dst)
cv.waitKey(0)
cv.destroyAllWindows()
