import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

ima=cv.imread('colors.jpg')

imagray=cv.cvtColor(ima,cv.COLOR_BGR2GRAY)
imahsv=cv.cvtColor(ima,cv.COLOR_BGR2HSV)

#
cv.imshow('ORIGINAL',ima)
cv.imshow('GRAY',imagray)
cv.imshow('HSV',imahsv)

k=cv.waitKey(0) & 0xFF

