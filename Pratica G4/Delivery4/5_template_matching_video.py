import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

cap = cv.VideoCapture('robocup2.mp4')
template = cv.imread('ball_small.png', 0)
template_canny = cv.Canny(template, 50, 150, apertureSize = 7)
w = template.shape[1]
h = template.shape[0]

cv.imshow('Template (Canny)', template_canny)

while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    # Apply Canny edge
    frame_bn = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_canny = cv.Canny(frame_bn, 50, 150, apertureSize = 7)
    
    # Apply template Matching
    res = cv.matchTemplate(frame_canny, template_canny, cv.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    
    top_left = max_loc
    
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv.rectangle(frame, top_left, bottom_right, 255, 2)
    
    cv.imshow('Ball detection', frame)

    k = cv.waitKey(25) & 0xFF
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()