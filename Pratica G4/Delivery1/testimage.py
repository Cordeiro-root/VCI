import numpy as np
import cv2 as cv

cam=cv.VideoCapture(0)
img_counter=0

while True:
	ret, frame=cam.read()
	frame = cv.flip(frame, 1)
	
	cv.imshow('Foto',frame)
	
	#
	if not ret:
		break
	k=cv.waitKey(1)
	
	if k%256==27:
		#ESC pressed
		print("Escape hit, closing...")
		break
	
	elif k%256==32:
		#space pressed
		img_name="frame.png".format(img_counter)
		cv.imwrite(img_name, frame)
		print("{} written!".format(img_name))
		img_counter += 1
cam.release()
          

#img1 over img2
img1 = cv.imread('frame1.png')
img2 = cv.imread('frame.png')

dst = cv.addWeighted(img1,0.7,img2,0.5,0)

cv.imshow('dst',dst)
cv.waitKey(0)
cv.destroyAllWindows()
