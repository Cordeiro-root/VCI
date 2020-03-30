import numpy as np
import cv2 as cv

yellow=np.uint8([[[32,185,246]]])
hsv_yellow=cv.cvtColor(yellow,cv.COLOR_BGR2HSV)
print('y=', hsv_yellow)

blue=np.uint8([[[157,145,82]]])
hsv_blue=cv.cvtColor(blue,cv.COLOR_BGR2HSV)
print('b=',hsv_blue)

red=np.uint8([[[61,55,117]]])
hsv_red=cv.cvtColor(red,cv.COLOR_BGR2HSV)
print('r=',hsv_red)

green=np.uint8([[[106,135,95]]])
hsv_green=cv.cvtColor(green,cv.COLOR_BGR2HSV)
print('g=',hsv_green)

white=np.uint8([[[220,233,216]]])
hsv_white=cv.cvtColor(white,cv.COLOR_BGR2HSV)
print('w=',hsv_white)

