import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread('image.jpeg')
cv.imshow('img',img)
color = ('b','g','r')
for i,col in enumerate(color):
    histr = cv.calcHist([img],[i],None,[256],[0,256])
    plt.plot(histr,color = col)
    plt.xlim([0,256])
plt.show()


