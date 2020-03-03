import numpy as np
import cv2 as cv
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    #gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame = cv.flip(frame, 1)
    
    #get image from file
    #image and video must be the same syze (640x480)
    img = cv.imread('image.png')
    #control the intensity of each image
    dst = cv.addWeighted(frame,0.7,img,0.3,0)
    # Display the resulting frame
    cv.imshow('dst', dst)
    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()

