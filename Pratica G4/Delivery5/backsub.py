from __future__ import print_function
import cv2 as cv

backSub = cv.createBackgroundSubtractorKNN()

capture = cv.VideoCapture('video.mp4')

if not capture.isOpened:
    exit(0)

while True:
    ret, frame = capture.read()
    if frame is None:
        break
    frame = cv.resize(frame, (1080, 700))
    fgMask = backSub.apply(frame)
    
    cv.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
    cv.putText(frame, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
    
    cv.imshow('Frame', frame)
    cv.imshow('FG Mask', fgMask)
    
    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break