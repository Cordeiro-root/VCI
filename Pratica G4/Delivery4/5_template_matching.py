import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

image = cv.imread('robo.png', 0)
template = cv.imread('ball.png', 0)

w = template.shape[1]
h = template.shape[0]

# All the 6 methods for comparison in a list
methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
           'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']

for meth in methods:
    method = eval(meth)
    
    # Apply Canny edge
    edgesI = cv.Canny(image, 50, 150, apertureSize = 7)
    edgesT = cv.Canny(template, 50, 150, apertureSize = 7)
    
    # Apply template Matching
    res = cv.matchTemplate(edgesI, edgesT, method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
        
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv.rectangle(image, top_left, bottom_right, 255, 2)
    
    plt.subplot(121), plt.imshow(res, cmap = 'gray')
    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(image, cmap = 'gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.suptitle(meth)
    plt.show()
    
################################################################################    
# Problems:                                                                    #
# 1) What if the in the image there is the object in the template but rescaled,#
#    or rotated?                                                               #
# 2) Also, problem with colors                                                 #
# 3) Computationally expensive                                                 #
################################################################################