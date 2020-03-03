import numpy as np
import cv2 as cv

def event(value):
    pass

cv.namedWindow('Color Calibration')
cv.createTrackbar('Contrast', 'Color Calibration', 0, 100, event)
cv.createTrackbar('Brightness', 'Color Calibration', 0, 255, event)
cv.createTrackbar('Saturation', 'Color Calibration', 0, 100, event)
#cv.createTrackbar('White Balance BLUE', 'Color Calibration', 0, 100, event)
#cv.createTrackbar('White Balance RED', 'Color Calibration', 0, 100, event)

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:

    # color calibration
    contrast = cv.getTrackbarPos('Contrast', 'Color Calibration')
    brightness = cv.getTrackbarPos('Brightness', 'Color Calibration')
    saturation = cv.getTrackbarPos('Saturation', 'Color Calibration')
    #whitebalanceB = cv.getTrackbarPos('White Balance BLUE', 'Color Calibration')
    #whitebalanceR = cv.getTrackbarPos('White Balance RED', 'Color Calibration')
    #whitebalance = cv.getTrackbarPos('White Balance', 'Color Calibration')

    ret, frame = cap.read()
    ret = cap.set(cv.CAP_PROP_CONTRAST, contrast)
    ret = cap.set(cv.CAP_PROP_BRIGHTNESS, brightness)
    ret = cap.set(cv.CAP_PROP_SATURATION, saturation)

    #ret = cap.set(cv.CAP_PROP_WHITE_BALANCE_BLUE_U, whitebalanceB)
    #ret = cap.set(cv.CAP_PROP_WHITE_BALANCE_RED_V, whitebalanceR)
    #ret = cap.set(cv.CAP_PROP_IOS_DEVICE_WHITEBALANCE, whitebalance)


    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
