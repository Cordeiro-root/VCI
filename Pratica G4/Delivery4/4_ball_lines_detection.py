import numpy as np
import cv2 as cv

def event(value):
    pass

cap = cv.VideoCapture('robocup2.mp4')

cv.namedWindow('Ball and lines')
cv.namedWindow('Parameters tuning')

cv.createTrackbar('param1(c)', 'Parameters tuning', 0, 200, event)
cv.setTrackbarPos('param1(c)', 'Parameters tuning', 100)
cv.createTrackbar('param2(c)', 'Parameters tuning', 0, 200, event)
cv.setTrackbarPos('param2(c)', 'Parameters tuning', 12)
cv.createTrackbar('minRad(c)', 'Parameters tuning', 0, 250, event)
cv.setTrackbarPos('minRad(c)', 'Parameters tuning', 0)
cv.createTrackbar('maxRad(c)', 'Parameters tuning', 0, 250, event)
cv.setTrackbarPos('maxRad(c)', 'Parameters tuning', 20)
cv.createTrackbar('Thresh(l)', 'Parameters tuning', 0, 200, event)
cv.setTrackbarPos('Thresh(l)', 'Parameters tuning', 100)
cv.createTrackbar('minLen(l)', 'Parameters tuning', 0, 200, event)
cv.setTrackbarPos('minLen(l)', 'Parameters tuning', 100)
cv.createTrackbar('maxGap(l)', 'Parameters tuning', 0, 200, event)
cv.setTrackbarPos('maxGap(l)', 'Parameters tuning', 10)

while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
    # 1) Identify the (yellow) ball
    
    low = np.array([26, 66, 97])
    high = np.array([46, 255, 208])
    mask = cv.inRange(hsv, low, high)
    
    res = cv.bitwise_and(frame, frame, mask = mask)
    
    edges = cv.Canny(res, 50, 150, apertureSize = 7)
    rows = edges.shape[0]
    p1 = cv.getTrackbarPos('param1(c)', 'Parameters tuning')
    p2 = cv.getTrackbarPos('param2(c)', 'Parameters tuning')
    m = cv.getTrackbarPos('minRad(c)', 'Parameters tuning')
    M = cv.getTrackbarPos('maxRad(c)', 'Parameters tuning')
    circles = cv.HoughCircles(edges, cv.HOUGH_GRADIENT, 1, rows / 8,
                              param1 = p1, param2 = p2,
                              minRadius = m, maxRadius = M)
        
    # 2) Identify the (white) lines
    
    low = np.array([35, 0, 182])
    high = np.array([87, 58, 255])
    mask = cv.inRange(hsv, low, high)
    
    res = cv.bitwise_and(frame, frame, mask = mask)
    
    edges = cv.Canny(res, 50, 150, apertureSize = 7)
    t = cv.getTrackbarPos('Thresh(l)', 'Parameters tuning')
    m = cv.getTrackbarPos('minLen(l)', 'Parameters tuning')
    M = cv.getTrackbarPos('maxGap(l)', 'Parameters tuning')
    lines = cv.HoughLinesP(edges, 1, np.pi / 180, t, minLineLength = m, maxLineGap = M)
    
    # 3) Display the frame
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        print('Found', circles.shape[1], 'circles for these parameters')

        for i in circles[0, :]:
            # draw the outer circle
            cv.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            #cv.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)
    else:
        print('No circles found for these parameters')
       
    if lines is not None:
        print('Found', lines.shape[1], 'lines for these parameters')
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    else:
        print('No lines found for these parameters')
        
    cv.imshow('Ball and lines', frame)

    k = cv.waitKey(25) & 0xFF
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()
