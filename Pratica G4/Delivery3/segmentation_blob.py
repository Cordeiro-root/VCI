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
            # Segment yellow: [21, 40, 0], [51, 255, 255]
            low = np.array([26, 66, 97])
            high = np.array([51, 255, 255])
            mask += cv.inRange(hsv, low, high)
        if(p == 1):
            # Segment green: [62, 51, 102], [74, 110, 186]
            low = np.array([62, 51, 102])
            high = np.array([74, 110, 186])
            mask += cv.inRange(hsv, low, high)
        if(l == 1):
            # Segment white: [0, 0, 177], [66, 83, 249]
            low = np.array([35, 0, 182])
            high = np.array([87, 58, 255])
            mask += cv.inRange(hsv, low, high)
        if(c == 1):
            # Segment blue: [110, 50, 50], [130, 255, 255]
            low = np.array([88, 65, 124])
            high = np.array([100, 255, 255])
            mask += cv.inRange(hsv, low, high)
        if(o == 1):
            # Segment red: [163, 124, 0], [200, 255, 216]
            low = np.array([171, 102, 0])
            high = np.array([255, 255, 123])
            mask += cv.inRange(hsv, low, high)    
    
        # Bitwise-AND mask and original image
        res = cv.bitwise_and(frame, frame, mask = mask)
        res = cv.cvtColor(res, cv.COLOR_BGR2GRAY)
        
        # Enhance the brightness
        #res[res > 0] = 255
        
        # Morphological operation
        kernel = np.ones((5, 5), np.uint8)
        dilation=cv.dilate(res,kernel,iterations=1)
        opening = cv.morphologyEx(dilation, cv.MORPH_OPEN, kernel)
        
        dilation=cv.dilate(opening,kernel,iterations=1)
        
        cv.imshow('Image Segmentation with tresholding (esc to close)', res)
        cv.imshow('Image Segmentation with tresholding (esc to close)opening', opening)
        
        
                
        # Setup SimpleBlobDetector parameters.
        params = cv.SimpleBlobDetector_Params()
        
        #filter by color
        params.filterByColor=1
        params.blobColor=255
        
        #filter by circularity
        params.filterByCircularity = 1
        params.minCircularity = 0.1
        params.maxCircularity = 1   
        
        
        #create a detector with the parameters
        ver=(cv.__version__).split('.')
        if int(ver[0])<3:
        	
        	detector=cv.SimpleBlobDetector(params)
        else:
        	detector=cv.SimpleBlobDetector_create(params)
        	
        #detect blobs
        keypoints=detector.detect(dilation)
        
        #draw detected blobs
        im_with_keypoints=cv.drawKeypoints(dilation,keypoints,np.array([]),(0,0,255),cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        
        #show blobs
        cv.imshow("Keypoints", im_with_keypoints)
        
    k = cv.waitKey(25) & 0xFF
    if k == 27:
        break
    
cv.destroyAllWindows()
