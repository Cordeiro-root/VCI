import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

def nothing(x):
	pass
	
img = np.zeros((300,512,3),np.uint8)
cv.namedWindow('image')

#img = cv.imread('colors.jpg',1)
ret,thresh1=cv.threshold(img,127,255,cv.THRESH_BINARY)

cv.createTrackbar('Tresh', 'Image Segmentation with tresholding (esc to close)', 0, 255, nothing)

while(1):
	s=1
	cv.imshow('img',img)
	#cv.imshow('thresh1',thresh1)
	r=cv.getTrackbarPos('R','image')
	
	k=cv.waitKey(1) & 0xFF
	if k==27:
		break
		
	if s==0:
		img[:]=0
	else:
		img[:]=[r]
	
cv.destroyAllWindows()

