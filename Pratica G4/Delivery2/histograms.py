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
    cap = cv.VideoCapture(0)#root.fileName)
    #root.destroy()
    
    return cap

def showHist(f_BGR, f_YUV, f_HSV):
    (b, g, r) = cv.split(f_BGR)
    hist_BGR_b = cv.calcHist([b], [0], None, [256], [0, 255])
    hist_BGR_g = cv.calcHist([g], [0], None, [256], [0, 255])
    hist_BGR_r = cv.calcHist([r], [0], None, [256], [0, 255])
    R.set_ydata(hist_BGR_r)
    G.set_ydata(hist_BGR_g)
    B.set_ydata(hist_BGR_b)
    
    (y, u, v) = cv.split(f_YUV)
    hist_YUV_y = cv.calcHist([y], [0], None, [256], [0, 255])
    hist_YUV_u = cv.calcHist([u], [0], None, [256], [0, 255])
    hist_YUV_v = cv.calcHist([v], [0], None, [256], [0, 255])
    Y.set_ydata(hist_YUV_y)
    U.set_ydata(hist_YUV_u)
    V.set_ydata(hist_YUV_v)
    
    (h, s, v1) = cv.split(f_HSV)
    hist_HSV_h = cv.calcHist([h], [0], None, [256], [0, 255])
    hist_HSV_s = cv.calcHist([s], [0], None, [256], [0, 255])
    hist_HSV_v1 = cv.calcHist([v1], [0], None, [256], [0, 255])
    H.set_ydata(hist_HSV_h)
    S.set_ydata(hist_HSV_s)
    V1.set_ydata(hist_HSV_v1)
    
    fig.canvas.draw()

    return

###############################################

# Load the video
cap = loadVideo()

# Initialize plot.
fig, ax = plt.subplots(1, 3, figsize = (40, 10))
fig.canvas.set_window_title('Real time histograms')

ax[0].set_title('Histogram (RGB)')
ax[0].set_xlabel('Intensity value')
ax[0].set_ylabel('Frequency')
ax[0].set_xlim(0, 256 - 1)
ax[0].set_ylim(0, 640 * 480)
ax[0].tick_params(axis = 'y', labelsize = 6)
R, = ax[0].plot(np.arange(256), np.zeros((256,)), c = 'r', label = 'Red')
G, = ax[0].plot(np.arange(256), np.zeros((256,)), c = 'g', label = 'Green')
B, = ax[0].plot(np.arange(256), np.zeros((256,)), c = 'b', label = 'Blue')
ax[0].legend()

ax[1].set_title('Histogram (YUV)')
ax[1].set_xlabel('Intensity value')
ax[1].set_ylabel('Frequency')
ax[1].set_xlim(0, 256 - 1)
ax[1].set_ylim(0, 640 * 480)
ax[1].tick_params(axis = 'y', labelsize = 6)
Y, = ax[1].plot(np.arange(256), np.zeros((256,)), c = 'y', label = 'Luma')
U, = ax[1].plot(np.arange(256), np.zeros((256,)), c = 'b', label = 'Blue projection')
V, = ax[1].plot(np.arange(256), np.zeros((256,)), c = 'r', label = 'Red projection')
ax[1].legend()

ax[2].set_title('Histogram (HSV)')
ax[2].set_xlabel('Intensity value')
ax[2].set_ylabel('Frequency')
ax[2].set_xlim(0, 256 - 1)
ax[2].set_ylim(0, 640 * 480)
ax[2].tick_params(axis = 'y', labelsize = 6)
H, = ax[2].plot(np.arange(256), np.zeros((256,)), c = 'r', label = 'Hue')
S, = ax[2].plot(np.arange(256), np.zeros((256,)), c = 'g', label = 'Saturation')
V1, = ax[2].plot(np.arange(256), np.zeros((256,)), c = 'b', label = 'Value')
ax[2].legend()

plt.ion()
plt.show()

# Play the video
while cap.isOpened():        
    ret, frame = cap.read()
    
    # If frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    # Convert the frame to YUV
    f_YUV = cv.cvtColor(frame, cv.COLOR_BGR2YUV)

    # Convert the frame to HSV 
    f_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
    # Show the frames        
    cv.imshow('BGR (press q to close)...', frame)
    cv.imshow('YUV (press q to close)...', f_YUV)
    cv.imshow('HSV (press q to close)...', f_HSV)
    
    # Show the histograms
    showHist(frame, f_YUV, f_HSV)
        
    if cv.waitKey(25) == ord('q'):
        break
        
cap.release()
cv.destroyAllWindows()
plt.close()
