# Implement an algorithm to perform multi-object tracking. Start by using the 
# developed object detection algorithms during the previous deliverables and 
# implement a solution that should be able to distinguish which objects are 
# being tracked (multiple balls and robots; assigning an unique ID to each 
# one,  etc)

import numpy as np
import cv2 as cv

###############################################################################
#                               FUNCTIONS                                     #
###############################################################################

def event(value):
    pass

def detect_color(img, color):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    low = np.array([0, 0, 0])
    high = np.array([0, 0, 0])
    
    if(color == 'light blue'):
        low = np.array([80, 80, 80])
        high = np.array([95, 195, 195])
    if(color == 'red/yellow/orange'):
        low = np.array([0, 93, 52])
        high = np.array([40, 236, 255])
    
    mask = cv.inRange(hsv, low, high)
    res = cv.bitwise_and(frame, frame, mask = mask)
    
    return cv.cvtColor(res, cv.COLOR_BGR2GRAY)

def good_shapes(arr, mode):
    to_return = []
    
    for c in arr:
        peri = cv.arcLength(c, True)
        approx = cv.approxPolyDP(c, 0.04 * peri, True)
        
        if(mode == 'rect' and len(approx) == 4):
			# 4-vertex polygon
            to_return.append(approx)
        if(mode == 'circ' and len(approx) >= 5):
            # circle
            to_return.append(approx)
            
    return to_return

def extract_rectangles(arr):
    to_return = []
    
    for c in arr:
        top = 700
        bottom = 0
        left = 1080
        right = 0
        for point in c:
            if(point[0][0] > right):
                right = point[0][0]
            if(point[0][0] < left):
                left = point[0][0]
            if(point[0][1] > bottom):
                bottom = point[0][1]
            if(point[0][1] < top):
                top = point[0][1]
                
        # Remove rectangles with shape clearly wrong
        if(bottom - top != 0 and right - left != 0):
            if((bottom - top) / (right - left) <= 2 and (right - left) / (bottom - top) <= 2):
                to_return.append([(left, top), (right, bottom)]) 
    
    return to_return

def display_bboxes(frame, arr, color):
    for b in arr:
        cv.rectangle(frame, (b[0][0], b[0][1]), (b[1][0], b[1][1]), color, 3)
    
    return

def remove_small(arr):
    to_return = []
    
    areas = [(b[1][0] - b[0][0]) * (b[1][1] - b[0][1]) for b in arr]
    area_avg = np.mean(areas)
    i = 0
    for a in areas:
        if(a > area_avg / 3):
            to_return.append(arr[i])
        i += 1
    
    return to_return

###############################################################################
#                                   MAIN                                      #
###############################################################################

cap = cv.VideoCapture('video.mp4')

cv.namedWindow('Object tracking')

while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        print('End of the video...')
        break
    
    frame = cv.resize(frame, (1080, 700))
    
    # 1) Contour detection (Robots)
    res = detect_color(frame, 'light blue')    
    contours_robots, hierarchy = cv.findContours(res, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    # 2) Contour detection (Balls)
    res = detect_color(frame, 'red/yellow/orange')    
    contours_balls, hierarchy = cv.findContours(res, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    # 3) Keep only good shapes
    good_contours_robots = good_shapes(contours_robots, 'rect')
    good_contours_balls = good_shapes(contours_balls, 'circ')         
    
    # 4) Rectangles from contours
    bboxes_robots = extract_rectangles(good_contours_robots)
    bboxes_balls = extract_rectangles(good_contours_balls)
    
    # 5) Remove too small rectangles
    bboxes_robots = remove_small(bboxes_robots)
    bboxes_balls = remove_small(bboxes_balls)
    
    # 6) Tracking...
    
    # 7) Display the frame
    display_bboxes(frame, bboxes_robots, (255, 0, 0))
    display_bboxes(frame, bboxes_balls, (0, 0, 255))
    
    cv.imshow('Object tracking', frame)
    
    k = cv.waitKey(25) & 0xFF
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()