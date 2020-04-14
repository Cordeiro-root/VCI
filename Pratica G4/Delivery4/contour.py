import sys
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

img = cv.imread('robo.png')
imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 127, 255, 0)
_, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)


cv.imshow('ORIGINAL', imgray)
cv.drawContours(img, contours, -1, (0,255,0), 3)
cv.imshow('Contours', img) 
k=cv.waitKey(0) & 0xFF
