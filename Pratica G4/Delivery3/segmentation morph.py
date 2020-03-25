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
cap = cv.VideoCapture('robocup.mp4')
cv.namedWindow('Segmentation (esc to close)')

# Mot important colors for cambada:
# (1) Yellow (ball)
# (2) Green (pitch)
# (3) White (lines)
# (4) Blue/Black/Red (players)

# Create trackbars for the tresholds
cv.createTrackbar('Ball', 'Segmentation (esc to close)', 0, 1, nothing)
cv.createTrackbar('Pitch', 'Segmentation (esc to close)', 0, 1, nothing)
cv.createTrackbar('Lines', 'Segmentation (esc to close)', 0, 1, nothing)
cv.createTrackbar('CAMBADA', 'Segmentation (esc to close)', 0, 1, nothing)
cv.createTrackbar('Opponents', 'Segmentation (esc to close)', 0, 1, nothing)

img = np.zeros((150, 640))
cv.putText(img, '1) Double click here to open the video', (20, 50), 
           cv.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1)
cv.putText(img, '2) Select which object you want to segment', (20, 105), 
           cv.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1)
cv.imshow('Segmentation (esc to close)', img)

flag = False

while(1):
    if cap.isOpened():
        ret, frame = cap.read()
    else:
        break
    
    cv.setMouseCallback('Segmentation (esc to close)', action)
    
    if(flag):
        b = cv.getTrackbarPos('Ball', 'Segmentation (esc to close)')
        p = cv.getTrackbarPos('Pitch', 'Segmentation (esc to close)')
        l = cv.getTrackbarPos('Lines', 'Segmentation (esc to close)')
        c = cv.getTrackbarPos('CAMBADA', 'Segmentation (esc to close)')
        o = cv.getTrackbarPos('Opponents', 'Segmentation (esc to close)')
        
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        
        low = np.array([0, 0, 0])
        high = np.array([[0, 0, 0]])
        mask = cv.inRange(hsv, low, high)
        
        if(b == 1):
            # Segment yellow: [26, 66, 97], [46, 255, 208]
            low = np.array([26, 66, 97])
            high = np.array([46, 255, 208])
            mask += cv.inRange(hsv, low, high)
        if(p == 1):
            # Segment green: [62, 51, 102], [74, 110, 186]
            low = np.array([62, 51, 102])
            high = np.array([74, 110, 186])
            mask += cv.inRange(hsv, low, high)
        if(l == 1):
            # Segment white: [35, 0, 182], [87, 58, 255]
            low = np.array([35, 0, 182])
            high = np.array([87, 58, 255])
            mask += cv.inRange(hsv, low, high)
        if(c == 1):
            # Segment blue: [88, 65, 124], [100, 255, 255]
            low = np.array([88, 65, 124])
            high = np.array([100, 255, 255])
            mask += cv.inRange(hsv, low, high)
        if(o == 1):
            # Segment red: [171, 102, 0], [255, 255, 123]
            low = np.array([171, 102, 0])
            high = np.array([255, 255, 123])
            mask += cv.inRange(hsv, low, high)    
    
        # Bitwise-AND mask and original image
        res = cv.bitwise_and(frame, frame, mask = mask)
        res = cv.cvtColor(res, cv.COLOR_BGR2GRAY)
        
        # Enhance the brightness
        #res[res > 0] = 255
        
        # Morphological operation
        kernel = np.ones((3, 3), np.uint8)
        opening = cv.morphologyEx(res, cv.MORPH_OPEN, kernel)
        
        cv.imshow('Image Segmentation with tresholding (esc to close)', res)
        cv.imshow('Image Segmentation with tresholding (esc to close)opening', opening)
        
        
    k = cv.waitKey(25) & 0xFF
    if k == 27:
        break
    
cv.destroyAllWindows()
