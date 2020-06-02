import numpy as np
import cv2 as cv

###############################################################################
#                               CONSTANTS                                     #
###############################################################################

# Frame height
h = 450

# Frame width
w = 540

# Parameters for Lucas-Kanade optical flow
lk_params = dict(winSize = (15,15), maxLevel = 2, criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

# Filename
filenames = ['video.mp4', '..//Delivery4//robocup2.mp4', 'video1.mov']
f = 0

###############################################################################
#                               FUNCTIONS                                     #
###############################################################################

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
    res = cv.bitwise_and(img, img, mask = mask)
    
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
        top = h
        bottom = 0
        left = w
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
                to_return.append((left, top, right, bottom))
    
    return to_return

def remove_small(arr):
    to_return = []
    
    areas = [(b[2] - b[0]) * (b[3] - b[1]) for b in arr]
    area_avg = np.mean(areas)
    i = 0
    for a in areas:
        if(a > area_avg / 4):
            to_return.append(arr[i])
        i += 1
    
    return to_return

###############################################################################
#                                   MAIN                                      #
###############################################################################
# Read first frame
cap = cv.VideoCapture('video.mp4')
ret, frame= cap.read()

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

print(bboxes_robots)
print(bboxes_balls)

# 6) Multi_Tracking
tracker= cv.MultiTracker_create()
tracker_type = cv.TrackerKCF_create()
for robot in bboxes_robots:
    tracker.add(tracker_type, frame, robot)

for balls in bboxes_balls:
    tracker.add(tracker_type, frame, balls)

cv.imshow('MultiTracker', frame)

while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        print('End of the video...')
        break
    
    frame = cv.resize(frame, (w, h))
    
    success, boxes= tracker.update(frame)

    
    for i, newbox in enumerate(bboxes_robots):
        p1 = (int(newbox[0]), int(newbox[1]))
        p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        cv.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
    
    cv.imshow('MultiTracker', frame)

    k = cv.waitKey(25) & 0xFF
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()