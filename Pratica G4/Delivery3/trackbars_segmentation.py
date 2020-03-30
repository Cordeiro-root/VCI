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
frame=cv.imread('puzzle.jpg')
#cap = cv.VideoCapture('robocup.mp4')
cv.namedWindow('Set the tresholds (esc to close)')

# Mot important colors for cambada:
# (1) Yellow (ball)
# (2) Green (pitch)
# (3) White (lines)
# (4) Blue/Black/Red (players)

# Create trackbars for the tresholds
cv.createTrackbar('H (low)', 'Set the tresholds (esc to close)', 0, 255, nothing)
cv.createTrackbar('S (low)', 'Set the tresholds (esc to close)', 0, 255, nothing)
cv.createTrackbar('V (low)', 'Set the tresholds (esc to close)', 0, 255, nothing)
cv.createTrackbar('H (high)', 'Set the tresholds (esc to close)', 0, 255, nothing)
cv.setTrackbarPos('H (high)', 'Set the tresholds (esc to close)', 255)
cv.createTrackbar('S (high)', 'Set the tresholds (esc to close)', 0, 255, nothing)
cv.setTrackbarPos('S (high)', 'Set the tresholds (esc to close)', 255)
cv.createTrackbar('V (high)', 'Set the tresholds (esc to close)', 0, 255, nothing)
cv.setTrackbarPos('V (high)', 'Set the tresholds (esc to close)', 255)

img = np.zeros((250, 640))
cv.putText(img, 'Double click here to open the video', (20, 55), 
           cv.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1)
cv.putText(img, 'Approx. color tresholds:', (20, 80), 
           cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
cv.putText(img, 'Blue -> [88, 65, 124], [100, 255, 255]', (40, 105), 
           cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
cv.putText(img, 'Yellow -> [26, 66, 97], [46, 255, 208]', (40, 130), 
           cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
cv.putText(img, 'White -> [35, 0, 182], [87, 58, 255]', (40, 155), 
           cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
cv.putText(img, 'Green -> [62, 51, 102], [74, 110, 186]', (40, 180), 
           cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
cv.putText(img, 'Red -> [171, 102, 0], [255, 255, 123]', (40, 205), 
           cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
cv.imshow('Set the tresholds (esc to close)', img)

flag = False

while(1):
    #if cap.isOpened():
     #   ret, frame = cap.read()
    #else:
    #    break
    
    cv.setMouseCallback('Set the tresholds (esc to close)', action)
    
    if (flag):
        hl = cv.getTrackbarPos('H (low)', 'Set the tresholds (esc to close)')
        sl = cv.getTrackbarPos('S (low)', 'Set the tresholds (esc to close)')
        vl = cv.getTrackbarPos('V (low)', 'Set the tresholds (esc to close)')
        hh = cv.getTrackbarPos('H (high)', 'Set the tresholds (esc to close)')
        sh = cv.getTrackbarPos('S (high)', 'Set the tresholds (esc to close)')
        vh = cv.getTrackbarPos('V (high)', 'Set the tresholds (esc to close)')
        
        low = np.array([hl, sl, vl])
        high = np.array([hh, sh, vh])
        
        gauss = cv.GaussianBlur(frame,(15,15),0)
        hsv = cv.cvtColor(gauss, cv.COLOR_BGR2HSV)
        
        # Threshold the HSV image to get only blue colors
        mask = cv.inRange(hsv, low, high)
    
        # Bitwise-AND mask and original image
        res = cv.bitwise_and(frame, frame, mask = mask)
        
        cv.imshow('Image Segmentation with tresholding (esc to close)', res)
        
    k = cv.waitKey(25) & 0xFF
    if k == 27:
        break
    
cv.destroyAllWindows()
