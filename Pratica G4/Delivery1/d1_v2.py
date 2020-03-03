import numpy as np
import cv2 as cv
import tkinter as tk
from tkinter import filedialog as fd

############ FUNCTIONS ###################################
size = (640, 480)

def applyWatermark(frame):
    cv.circle(frame, (size[0] - 60, size[1] - 60), 50, (255, 150, 150), -1)
    cv.putText(frame, 'G4', (size[0] - 100, size[1] - 40), cv.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 10)
    return

def event(val):
    pass

def recordVideo(filename, cam = 0, size = (640, 480), fps = 20, cal = False):
    cap = cv.VideoCapture(cam)
    
    # Define the codec and create VideoWriter object
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    out = cv.VideoWriter(filename, fourcc, fps, size)

    if not cap.isOpened():
        print('Cannot open camera')
        exit()
	
    while True:            
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        # Color calibration
        # https://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-get
        
        c = cv.getTrackbarPos('Contrast', 'Menu')
        b = cv.getTrackbarPos('Brightness', 'Menu')
        s = cv.getTrackbarPos('Saturation', 'Menu')
    
    
        ret = cap.set(cv.CAP_PROP_CONTRAST, c)
        ret = cap.set(cv.CAP_PROP_BRIGHTNESS, b)
        ret = cap.set(cv.CAP_PROP_SATURATION, s)
	
        # If frame is read correctly ret is True
        if not ret:
            print('Can\'t receive frame (stream end?). Exiting ...')
            break
	
    	# Flip the frame ('mirror effect')
        frame = cv.flip(frame, 1)
	
    	# Watermark
        # https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_core/py_image_arithmetics/py_image_arithmetics.html?highlight=blend
        applyWatermark(frame)
	
    	# Write the flipped frame
        out.write(frame)
 
        # Display the resulting frame
        cv.imshow('Acquiring video (press q to close)...', frame)
	
        # Wait for a key to exit
        if cv.waitKey(1) == ord('q'):
            break
		
    # When everything is done, release the capture
    cap.release()
    out.release()
    cv.destroyWindow('Acquiring video (press q to close)...')
    
    return

def playVideo(filename):
    cap = cv.VideoCapture(filename)
    
    while cap.isOpened():        
        ret, frame = cap.read()
            
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        
        cv.imshow('Showing video (press q to close)...', frame)
        
        if cv.waitKey(25) == ord('q'):
            break
        
    cap.release()
    cv.destroyWindow('Showing video (press q to close)...')
    
    return

################################################################
    
# Initial menu
cv.namedWindow('Menu')
cv.createTrackbar('Record', 'Menu' , 0, 1, event)
cv.setTrackbarPos('Record', 'Menu', 0)
cv.createTrackbar('Play', 'Menu' , 0, 1, event)
cv.setTrackbarPos('Play', 'Menu', 0)
cv.createTrackbar('Contrast', 'Menu', 0, 100, event)
cv.setTrackbarPos('Contrast', 'Menu', 0)
cv.createTrackbar('Brightness', 'Menu', 0, 255, event)
cv.setTrackbarPos('Brightness', 'Menu', 0)
cv.createTrackbar('Saturation', 'Menu', 0, 100, event)
cv.setTrackbarPos('Saturation', 'Menu', 0)
img = np.zeros((350, 600, 3))
img = cv.putText(img, 'Record: record a new video', (0, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
img = cv.putText(img, 'Play: play an old video', (0, 70), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
img = cv.putText(img, 'Contrast/Brightness/Saturation:', (0, 110), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
img = cv.putText(img, 'color calibration', (0, 150), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
img = cv.putText(img, "(Press 'esc' to close the program)", (0, 190), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
cv.circle(img, (600 - 70, 350 - 70), 50, (255, 150, 150), -1)
cv.putText(img, 'G4', (600 - 110, 350 - 50), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 10)
cv.imshow('Menu', img)

while(1):
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break

    # Get current positions of trackbars
    r = cv.getTrackbarPos('Record', 'Menu')
    p = cv.getTrackbarPos('Play', 'Menu')

    if(r == 1):
        recordVideo('output.avi')
        cv.setTrackbarPos('Record', 'Menu', 0)
    if(p == 1):
        root = tk.Tk()
        root.fileName = fd.askopenfilename(filetypes = (('Video files', '*.avi'), ('All files', '*.*')))
        playVideo(root.fileName)
        root.destroy()
        cv.setTrackbarPos('Play', 'Menu', 0)
        
cv.destroyAllWindows()
