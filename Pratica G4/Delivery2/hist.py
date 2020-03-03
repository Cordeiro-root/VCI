import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

ima=cv.imread('image.jpeg')
cv.imshow('ima',ima)

plt.hist(ima.ravel(),256,[0,256])
plt.show()

k=cv.waitKey(0) & 0xFFsdf

