import cv2 as cv
import numpy as np

def nothing(x):
    pass

def action(event, x, y, flags, param):
    global flag
    if event == cv.EVENT_LBUTTONDBLCLK:
        flag = not flag
    return

# Create a black image, a window
cap = cv.VideoCapture(0)
cv.namedWindow('Image Segmentation with tresholding (esc to close)')

# Create trackbars for the tresholds
cv.createTrackbar('Tresh', 'Image Segmentation with tresholding (esc to close)', 0, 255, nothing)
#cv.createTrackbar('Green', 'Image Segmentation with tresholding (esc to close)', 0, 255, nothing)
#cv.createTrackbar('Blue', 'Image Segmentation with tresholding (esc to close)', 0, 255, nothing)

flag = False

while(1):
    if cap.isOpened():
        ret, frame = cap.read()
        frame = cv.flip(frame, 1)
        #frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    else:
        break
        
    if(not flag):
        cv.imshow('Image Segmentation with tresholding (esc to close)', frame)
    else:
        t = cv.getTrackbarPos('Tresh', 'Image Segmentation with tresholding (esc to close)')
        #g = cv.getTrackbarPos('Green', 'Image Segmentation with tresholding (esc to close)')
        #b = cv.getTrackbarPos('Blue', 'Image Segmentation with tresholding (esc to close)')
        
        frame[frame < t] = 0
        frame[frame >= t] = 255
        
        cv.imshow('Image Segmentation with tresholding (esc to close)', frame)
            
    cv.setMouseCallback('Image Segmentation with tresholding (esc to close)', action)
        
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break
    
cv.destroyAllWindows()
