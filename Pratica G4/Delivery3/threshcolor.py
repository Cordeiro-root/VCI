import numpy as np
import cv2 as cv

def nothing(x):
	pass

#create a black image, a window
#img = np.zeros((300,512,3),np.uint8)
img=cv.imread('colors.jpg',1)
#ret,thresh1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
cv.namedWindow('image')
#creat trackbars for color change
cv.createTrackbar('R','image',0,255,nothing)
#cv.createTrackbar('G','image',0,255,nothing)
#cv.createTrackbar('B','image',0,255,nothing)

# create switch for ON/OFF functionality
switch='0 : OFF \n1 : ON'
cv.createTrackbar(switch,'image',0,1,nothing)

while(1):
	cv.imshow('orimage',img)
	cv.imshow('image',thresh1)
	k=cv.waitKey(1) & 0xFF
	if k==27:
		break
		
	#get current position of four trackbars
	r=cv.getTrackbarPos('R','image')
	#g=cv.getTrackbarPos('G','image')
	#b=cv.getTrackbarPos('B','image')
	s=cv.getTrackbarPos(switch,'image')		
	
	if s==0:
		img[:]=0
	else:
		img[:]=[0,0,r]
	
cv.destroyAllWindows()
