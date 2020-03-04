import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

while True:
	img = cv.imread('image.jpeg',0)
	equ = cv.equalizeHist(img)
	res = np.hstack((img,equ)) #stacking images side-by-side
	#cv.imwrite('res.png',res)
	cv.imshow('Compare',res)

	if cv.waitKey(1) == ord('q'):
	    break
# When everything done, release the capture 
cv.destroyAllWindows()
