import numpy as np
import cv2 as cv

def whiteBalance(frame):
    #print(frame.shape)
	#M = np.array([[255 / ], ])
    return frame

cap = cv.VideoCapture(1) # 0: back camera, 1: front camera

# Size of the images
size = (640, 480)

# Define the codec and create VideoWriter object
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('output.avi', fourcc, 20.0, size)

 #Logo to superimpose as watermark
#logo = cv.imread('logo.png', 1)
#logo += 200
#padding = np.zeros((logo.shape[0], size[0] - logo.shape[1], 3), dtype = 'uint8')
#logo = np.concatenate((padding, logo), axis = 1)
#padding = np.zeros((size[1] - logo.shape[0], size[0], 3), dtype = 'uint8')
#logo = np.concatenate((padding, logo), axis = 0)

if not cap.isOpened():
    print('Cannot open camera')
    exit()
	
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
	
    # If frame is read correctly ret is True
    if not ret:
        print('Can\'t receive frame (stream end?). Exiting ...')
        break
	
	# Flip the frame ('mirror effect')
    frame = cv.flip(frame, 1)
	
	# Color calibration????? https://stackoverflow.com/questions/45926871/webcam-color-calibration-using-opencv
    #frame = whiteBalance(frame)
	
	# Watermark : https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_core/py_image_arithmetics/py_image_arithmetics.html?highlight=blend
    #frame += logo
    cv.circle(frame, (size[0] - 60, size[1] - 60), 50, (255, 150, 150), -1)
    cv.putText(frame, 'G4', (size[0] - 100, size[1] - 40), 	        cv.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 10)
	
	# Write the flipped frame
    out.write(frame)
 
    # Display the resulting frame
    cv.imshow('Acquiring video...', frame)
	
	# Wait for a key to exit
    if cv.waitKey(1) == ord('q'):
        break
		
# When everything is done, release the capture
cap.release()
out.release()
cv.destroyAllWindows()
