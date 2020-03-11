import numpy as np
import cv2 as cv

drawing=False #true if mouse is pressed
mode=True #if Tru, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1,-1

#mouse callback function
def draw_circle(event,x,y,flags,param):
	global ix,iy,drawing,mode
	
	if event==cv.EVENT_LBUTTONDOWN:
		drawing=True
		ix,iy=x,y
	
	elif event==cv.EVENT_MOUSEMOVE:
		if drawing == True:
			if mode
