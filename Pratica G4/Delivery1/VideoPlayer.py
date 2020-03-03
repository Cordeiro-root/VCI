import numpy as np
import cv2 as cv

def captureVideo():
	print("\nPress 's' to start and stop saving video\n")
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
		  frame = cv.flip(frame, 1)
		  # Display the resulting frame
		  cv.imshow('frame', frame)
		  if cv.waitKey(1) == ord('s'):
		      break

	# When everything done, release the capture
	cap.release()
	#cv.destroyAllWindows()
	return

def saveVideo():
	#name=input("Name for the Video .avi?\n")
	cap = cv.VideoCapture(0)

	# Define the codec and create VideoWriter object
	fourcc = cv.VideoWriter_fourcc(*'XVID')
	out = cv.VideoWriter('output.avi', fourcc, 20.0, (640,  480))

	while cap.isOpened():
		  ret, frame = cap.read()
		  if not ret:
		      print("Can't receive frame (stream end?). Exiting ...")
		      break
		  frame = cv.flip(frame, 1) #virar cabeça para baixo '0', de lado '1'
		  # write the flipped frame
		  out.write(frame)
		  cv.imshow('frame', frame)
		  
		  if cv.waitKey(1) == ord('s'):
		    	break
		      
	cap.release()
	out.release()
	cv.destroyAllWindows()
	return 
	
def readVideo():
	video=input("\nWhat is the name of the Video .avi?\n")
	cap = cv.VideoCapture(video+'.avi')

	while cap.isOpened():
		  ret, frame = cap.read()
		  # if frame is read correctly ret is True
		  if not ret:
		      print("Can't receive frame (stream end?). Exiting ...")
		      break
		  cv.imshow('frame', frame)
		  if cv.waitKey(70) == ord('q'):
		      break
	cap.release()
	cv.destroyAllWindows()
	return

while (1):
	k=input("\nPress 'c' to capture Video\nPress 'r' to read Video Files\nPress 'q' to exit\n")
	
	if k=='c':
		captureVideo()
		saveVideo()
		print("Video saved as 'output'\n")
	
	elif k=='r':
		readVideo()
	
	elif k=='q':
		break
		
	else:
		print("CAN'T YOU READ???")
		
