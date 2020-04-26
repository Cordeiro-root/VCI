import os
import cv2
#import keras
import numpy as np
from keras.models import load_model
from keras import backend 

# calculates nms to get rid of overlapped boxes
def non_max_suppression(boxes, overlapThresh):
	# if there are no boxes, return an empty list
	if len(boxes) == 0:
		return []
	# if the bounding boxes integers, convert them to floats --
	# this is important since we'll be doing a bunch of divisions
	if boxes.dtype.kind == "i":
		boxes = boxes.astype("float")
	# initialize the list of picked indexes	
	pick = []
	# grab the coordinates of the bounding boxes
	x1 = boxes[:,0]
	y1 = boxes[:,1]
	x2 = boxes[:,2]
	y2 = boxes[:,3]
	# compute the area of the bounding boxes and sort the bounding
	# boxes by the bottom-right y-coordinate of the bounding box
	area = (x2 - x1 + 1) * (y2 - y1 + 1)
	idxs = np.argsort(y2)
	# keep looping while some indexes still remain in the indexes
	# list
	while len(idxs) > 0:
		# grab the last index in the indexes list and add the
		# index value to the list of picked indexes
		last = len(idxs) - 1
		i = idxs[last]
		pick.append(i)
		# find the largest (x, y) coordinates for the start of
		# the bounding box and the smallest (x, y) coordinates
		# for the end of the bounding box
		xx1 = np.maximum(x1[i], x1[idxs[:last]])
		yy1 = np.maximum(y1[i], y1[idxs[:last]])
		xx2 = np.minimum(x2[i], x2[idxs[:last]])
		yy2 = np.minimum(y2[i], y2[idxs[:last]])
		# compute the width and height of the bounding box
		w = np.maximum(0, xx2 - xx1 + 1)
		h = np.maximum(0, yy2 - yy1 + 1)
		# compute the ratio of overlap
		overlap = (w * h) / area[idxs[:last]]
		# delete all indexes from the index list that have
		idxs = np.delete(idxs, np.concatenate(([last],
			np.where(overlap > overlapThresh)[0])))
	# return only the bounding boxes that were picked using the
	# integer data type
	return boxes[pick].astype("int")

ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()
dataset_dir = 'robocup-MSL-dataset-master/VOC/'
images_dir = dataset_dir + 'JPEGImages/'
annotations_dir = dataset_dir + 'Annotations/'

# loads the trained model
model = load_model('detection.h5')

processing_image = 0
for filename in os.listdir(images_dir):
	if processing_image < 6: # just for the class demo
		print('Processing image ' + str(processing_image))
		img_path = images_dir + filename
		img= cv2.imread(img_path)

		resized_img = cv2.resize(img, (200,200))

		img_display = resized_img.copy()

		ss.setBaseImage(resized_img)
		ss.switchToSelectiveSearchFast()
		ssresults = ss.process()

		boxes = []
		scores = []
		for length, result in enumerate(ssresults):
			x,y,w,h = result
			roi=resized_img[y:y+h, x:x+w]
			roi = cv2.resize(roi, (224,224))
			img = np.expand_dims(roi, axis=0)
			# predicts rois as being robots or background using the loaded model
			prediction = model.predict(img)
			print(prediction)
			# threshold - index 0 is the probability of being background, index 1 is the probability of being a robot
			if prediction[0][1] > 0.99:
				# candidates
				boxes.append([x,y,x+w,y+h])
				cv2.rectangle(img_display, (x,y), (x+w,y+h), (0,255,0), 2)
				cv2.namedWindow('Candidates', cv2.WINDOW_NORMAL)
				cv2.resizeWindow('Candidates', 500, 500)
				cv2.imshow('Candidates', img_display)
				cv2.waitKey(30)

		boxes = np.array(boxes)
		nms_boxes = non_max_suppression(boxes, 0.3)
		for bb in nms_boxes:
			cv2.rectangle(resized_img, (bb[0],bb[1]), (bb[2],bb[3]), (0,0,255), 2)
		cv2.namedWindow('Final Result', cv2.WINDOW_NORMAL)
		cv2.resizeWindow('Final Result', 500, 500)
		cv2.imshow('Final Result', resized_img)
		cv2.waitKey()

	processing_image+=1

cv2.destroyAllWindows()
backend.clear_session()