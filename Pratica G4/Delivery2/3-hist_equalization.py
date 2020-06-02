import numpy as np
import cv2 as cv
import tkinter as tk
from tkinter import filedialog as fd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use( 'tkagg' ) # rendering to a canvas

############# Functions #######################

def loadVideo():
    #root = tk.Tk()
    #root.fileName = fd.askopenfilename(filetypes = (('Video files', '*.avi'), ('All files', '*.*')))
    #cap = cv.VideoCapture(root.fileName)
    cap = cv.VideoCapture(0)
    #root.destroy()
    
    return cap

def showHist(f_ORIGINAL, f_EQUALIZED):
    hist_or = cv.calcHist([f_ORIGINAL], [0], None, [256], [0, 255])
    OR.set_ydata(hist_or)
    
    hist_eq = cv.calcHist([f_EQUALIZED], [0], None, [256], [0, 255])
    EQ.set_ydata(hist_eq)
       
    fig.canvas.draw()

    return

###############################################

# Load the video
cap = loadVideo()

# Initialize plot.
fig, ax = plt.subplots(1, 2, figsize = (40, 10))
fig.canvas.set_window_title('Real time histograms')

ax[0].set_title('Histogram (original)')
ax[0].set_xlabel('Intensity value')
ax[0].set_ylabel('Frequency')
ax[0].set_xlim(0, 256 - 1)
ax[0].set_ylim(0, 640 * 480)
ax[0].tick_params(axis = 'y', labelsize = 6)
OR, = ax[0].plot(np.arange(256), np.zeros((256,)))

ax[1].set_title('Histogram (equalized)')
ax[1].set_xlabel('Intensity value')
ax[1].set_ylabel('Frequency')
ax[1].set_xlim(0, 256 - 1)
ax[1].set_ylim(0, 640 * 480)
ax[1].tick_params(axis = 'y', labelsize = 6)
EQ, = ax[1].plot(np.arange(256), np.zeros((256,)))

plt.ion()
plt.show()

# Play the video
while cap.isOpened():        
    ret, frame = cap.read()
    
    # If frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    # Convert to grayscale
    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    # Equalize
    f_eq = cv.equalizeHist(frame)
    
    # Show the frames
    cv.imshow('Acquiring grayscale video (press q to close)...', frame)
    cv.imshow('Equalized grayscale video (press q to close)...', f_eq)
    
    # Show the histograms
    showHist(frame, f_eq)
        
    if cv.waitKey(25) == ord('q'):
        break
        
cap.release()
cv.destroyAllWindows()
plt.close()
