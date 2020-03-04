import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use( 'tkagg' ) # rendering to a canvas


cap = cv2.VideoCapture('garden_sif.y4m')


bins=256
f,ax=plt.subplots()

hsv, ax_hsv = plt.subplots()


R, = ax.plot(np.arange(bins), np.zeros((bins,)), c='r',label='Red')
G, = ax.plot(np.arange(bins), np.zeros((bins,)), c='g',label='Green')
B, = ax.plot(np.arange(bins), np.zeros((bins,)), c='b',label='Blue')

H, = ax_hsv.plot(np.arange(bins), np.zeros((bins,)), c='r',label='Red')
S, = ax_hsv.plot(np.arange(bins), np.zeros((bins,)), c='g',label='Green')
V, = ax_hsv.plot(np.arange(bins), np.zeros((bins,)), c='b',label='Blue')

ax.set_xlim(0, bins-1)
ax.set_ylim(0, 2000)

ax_hsv.set_xlim(0, bins-1)
ax_hsv.set_ylim(0, 2000)

plt.ion() # Turn the interactive mode on
plt.show()

while(True):
	ret, frame = cap.read()
	if ret == True:		
		cv2.imshow('Video', frame)

		hsv_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
		(b,g,r) = cv2.split(frame)
		histR = cv2.calcHist([r], [0], None, [bins], [0, 255])
		histG = cv2.calcHist([g],[0],None,[bins],[0,255])
		histB = cv2.calcHist([b],[0],None,[bins],[0,255])

		(h,s,v) = cv2.split(hsv_frame)
		histH = cv2.calcHist([h], [0], None, [bins], [0, 255])
		histS = cv2.calcHist([s],[0],None,[bins],[0,255])
		histV = cv2.calcHist([v],[0],None,[bins],[0,255])

		R.set_ydata(histR)
		G.set_ydata(histG)
		B.set_ydata(histB)

		H.set_ydata(histH)
		S.set_ydata(histS)
		V.set_ydata(histV)


		f.canvas.draw()
		hsv.canvas.draw()
		if cv2.waitKey(1) & 0xFF == ord('q'): 
			break

	else:
		break

cap.release()
cv2.destroyAllWindows()
