import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)
#size of image
size = (640, 480)
# Define the codec and create VideoWriter object
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('output.avi', fourcc, 20.0, (640,  480))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # write the flipped frame
    frame = cv.flip(frame, 1) #virar cabeça para baixo '0', de lado '1'
    
    #Logo over image
    cv.circle(frame, (size[0]-60,size[1]-60),50,(255, 150,150),-1)
    cv.putText(frame, 'G4', (size[0] - 100, size[1] - 40), 	     cv.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 10)
    
    
    out.write(frame)
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break
        
# Release everything if job is finished
cap.release()
out.release()
cv.destroyAllWindows()
