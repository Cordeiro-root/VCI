import cv2 as cv
import numpy as np

###############################################################################
#                               CONSTANTS                                     #
###############################################################################

# Frame height
h = 700

# Frame width
w = 1080

# Parameters for Shi-Tomasi corner detection
feature_params = dict(maxCorners = 300, qualityLevel = 0.2, minDistance = 2, blockSize = 7)

# Parameters for Lucas-Kanade optical flow
lk_params = dict(winSize = (15,15), maxLevel = 2, criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

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

def extract_points(arr):
    #float32 is required by the optical flow function
    to_return = np.zeros((len(arr) * 2, 1, 2), dtype = 'float32')
    
    i = 0
    for t in arr:
        to_return[i, 0, 0] = t[0]
        to_return[i, 0, 1] = t[1]
        to_return[i+1, 0, 0] = t[2]
        to_return[i+1, 0, 1] = t[3]
        i +=1
    
    return to_return

def draw_optical_flow(new, old, color, mask, frame):
    # Draws the optical flow tracks for the robots
    for i, (n, o) in enumerate(zip(new, old)):
        # Returns a contiguous flattened array as (x, y) coordinates for new point
        a, b = n.ravel()
        # Returns a contiguous flattened array as (x, y) coordinates for old point
        c, d = o.ravel()
        # Draws line between new and old position with green color and 2 thickness
        mask = cv.line(mask, (a, b), (c, d), color, 2)
        # Draws filled circle (thickness of -1) at new position with green color and radius of 3
        frame = cv.circle(frame, (a, b), 3, color, -1)
        
    return mask, frame

def update_distance(prev_dist, new_points, old_points):
    if(new_points.shape == old_points.shape):
        to_return = prev_dist
        for n, o in zip(new_points, old_points):
            to_return += cv.norm(n, o, normType = cv.NORM_L2)
            
        return to_return
    else:
        return prev_dist

###############################################################################
#                                   MAIN                                      #
###############################################################################

# Read the first frame
cap = cv.VideoCapture('video.mp4')
#cap = cv.VideoCapture('..//Delivery4//robocup2.mp4')
ret, first_frame = cap.read()
# Resize the frame to fit the screen
first_frame = cv.resize(first_frame, (w, h))
prev_gray = cv.cvtColor(first_frame, cv.COLOR_BGR2GRAY)

# Finds objects in the first frame
# 1) Contour detection (Robots)
res = detect_color(first_frame, 'light blue')    
contours_robots, hierarchy = cv.findContours(res, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
# 2) Contour detection (Balls)
res = detect_color(first_frame, 'red/yellow/orange')    
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

prev_robots = extract_points(bboxes_robots)
prev_balls = extract_points(bboxes_balls)

# For later drawing purposes
mask = np.zeros_like(first_frame)
color_robots = (255, 0, 0)
color_balls = (0, 0, 255)

dist_img = np.zeros((200, 640))

# Distances
dist_team = 0
dist_balls = 0

cv.namedWindow('Optical flow')
cv.namedWindow('Travelled distance')

frame_counter = 1
while(cap.isOpened()):
    
    ret, frame = cap.read()
    if not ret:
        print('End of the video...')
        break
    
    # Resize the frame to fit the screen
    frame = cv.resize(frame, (w, h))
    
    # Converts each frame to grayscale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    # Calculates sparse optical flow by Lucas-Kanade method
    # https://docs.opencv.org/3.0-beta/modules/video/doc/motion_analysis_and_object_tracking.html#calcopticalflowpyrlk
    next_position_robots, status_robots, error_robots = cv.calcOpticalFlowPyrLK(prev_gray, gray, prev_robots, None, **lk_params)
    next_position_balls, status_balls, error_balls = cv.calcOpticalFlowPyrLK(prev_gray, gray, prev_balls, None, **lk_params)
    
    # Selects good feature points for previous position
    good_old_robots = prev_robots[status_robots == 1]
    good_old_balls = prev_balls[status_balls == 1]
    
    # Selects good feature points for next position
    good_new_robots = np.array([], dtype = 'float32')
    if(next_position_robots is not None):
        good_new_robots = next_position_robots[status_robots == 1]
        
    good_new_balls = np.array([], dtype = 'float32')
    if(next_position_balls is not None):
        good_new_balls = next_position_balls[status_balls == 1]
    
    # Update distances
    dist_team = update_distance(dist_team, good_new_robots, good_old_robots)
    dist_balls = update_distance(dist_balls, good_new_balls, good_old_balls)
    
    # Draw the optical flow
    mask_robots, frame = draw_optical_flow(good_new_robots, good_old_robots, color_robots, mask, frame)
    mask_balls, frame = draw_optical_flow(good_new_balls, good_old_balls, color_balls, mask, frame)
    
    # Overlays the optical flow tracks on the original frame
    output = cv.add(frame, mask_robots)
    output = cv.add(frame, mask_balls)
    
    # Updates previous frame
    prev_gray = gray.copy()
    
    # Updates previous good feature points
    prev_robots = good_new_robots.reshape(-1, 1, 2)
    prev_balls = good_new_balls.reshape(-1, 1, 2)
    
    # Opens a new window and displays the output frame
    cv.imshow('Optical flow', output)
    cv.putText(dist_img, 'Team distance: {:.2f} px'.format(dist_team), (10, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
    cv.putText(dist_img, 'Balls distance: {:.2f} px'.format(dist_balls), (10, 100), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
    cv.imshow('Travelled distance', dist_img)
    dist_img = np.zeros((200, 640))
    
    # Every 5 frames recompute the points to track, if new objects appeared or 
    # others disappeared
    if(frame_counter % 5 == 0):
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

        prev_robots = extract_points(bboxes_robots)
        prev_balls = extract_points(bboxes_balls)
    
    frame_counter += 1    
        
    # Frames are read by intervals of 10 milliseconds. The programs breaks out of the while loop when the user presses the 'q' key
    k = cv.waitKey(25) & 0xFF
    if k == 27:
        break
    
# Free up resources and closes all windows
cap.release()
cv.destroyAllWindows()