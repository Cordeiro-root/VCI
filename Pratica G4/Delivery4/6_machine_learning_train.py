import os
import cv2
import keras
import numpy as np
import tensorflow as tf
from keras import backend 
from keras.models import Model
from keras.layers import *
from xml.etree import ElementTree
from sklearn.model_selection import train_test_split
from keras.applications.resnet50 import ResNet50
from keras.callbacks import ModelCheckpoint

# Extracts the groundtruth boxes from the dataset
def extract_boxes(filename): 
	# load and parse the file
	tree = ElementTree.parse(filename)
	# get the root of the document
	root = tree.getroot()
	# extract each bounding box
	boxes = list()
	for box in root.findall('.//bndbox'):
		xmin = int(box.find('xmin').text)
		ymin = int(box.find('ymin').text)
		xmax = int(box.find('xmax').text)
		ymax = int(box.find('ymax').text)
		coors = [xmin, ymin, xmax, ymax]
		boxes.append(coors)

	# extract image dimensions
	width = int(root.find('.//size/width').text)
	height = int(root.find('.//size/height').text)
	return boxes, width, height

# Resizes bounding boxes according to the image resize
def resize_bbox(bbox, in_size, out_size):
	x_scale = out_size[0] / in_size[0]
	y_scale = out_size[1] / in_size[1]

	bbox[1] = int(y_scale * bbox[1])
	bbox[3] = int(y_scale * bbox[3])
	bbox[0] = int(x_scale * bbox[0])
	bbox[2] = int(x_scale * bbox[2])
	return bbox


# Calculates IOU
def intersection_over_union(boxA, boxB):
	# determine the (x, y)-coordinates of the intersection rectangle
	xA = max(boxA[0], boxB[0])
	yA = max(boxA[1], boxB[1])
	xB = min(boxA[2], boxB[2])
	yB = min(boxA[3], boxB[3])

	# compute the area of intersection rectangle
	interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
	# compute the area of both the prediction and ground-truth
	# rectangles
	boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
	boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
	# compute the intersection over union by taking the intersection
	# area and dividing it by the sum of prediction + ground-truth
	# areas - the interesection area
	iou = interArea / float(boxAArea + boxBArea - interArea)
	# return the intersection over union value
	return iou




ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()
dataset_dir = 'robocup-MSL-dataset-master/VOC/'
images_dir = dataset_dir + 'JPEGImages/'
annotations_dir = dataset_dir + 'Annotations/'


# make sure we have the same number of positive and negative samples
positives = 0
negatives = 0
images = []
labels = []
processing_image = 0
for filename in os.listdir(images_dir):
	if processing_image == 6: # just for the class demo, but can also control how the dataset is built
		break
		
	print('Processing image ' + str(processing_image))

	# extract image id
	image_id = filename[:-4]
	# setting image file
	img_path = images_dir + filename
	# setting annotations file
	ann_path = annotations_dir + image_id + '.xml'
	# get groundtruth boxes
	boxes, w, h = extract_boxes(ann_path)

	img = cv2.imread(img_path)

	resized_img = cv2.resize(img, (200,200))
	gt = resized_img.copy()
	region_proposals = resized_img.copy()
	final_rois = resized_img.copy()

	# resizes boxes as well
	scaled_boxes = []
	for box in boxes:
		new_box = resize_bbox(box, (img.shape[1], img.shape[0]), (200,200))
		scaled_boxes.append(new_box)
		cv2.rectangle(gt, (new_box[0],new_box[1]), (new_box[2],new_box[3]), (255,0,0), 2)
		cv2.rectangle(final_rois, (new_box[0],new_box[1]), (new_box[2],new_box[3]), (0,255,0), 2)
		# positive samples
		roi = resized_img[new_box[1]:new_box[3], new_box[0]:new_box[2]]
		roi = cv2.resize(roi, (224,224))
		images.append(roi)
		labels.append(1)
		positives += 1

	# region proposals
	ss.setBaseImage(resized_img)
	ss.switchToSelectiveSearchFast()
	ssresults = ss.process()

	for length, result in enumerate(ssresults):
		# negative samples
		if negatives < positives:
			x,y,w,h = result
			cv2.rectangle(region_proposals, (x,y), (x+w,y+h), (255,255,0), 2)
			iou = []
			for box in scaled_boxes:
				iou.append(intersection_over_union(box, [x,y,x+w,y+h]))

			if max(iou) == 0.0:
				cv2.rectangle(final_rois, (x,y), (x+w,y+h), (0,0,255), 2)
				roi = resized_img[y:y+h, x:x+w]
				roi = cv2.resize(roi, (224,224))
				images.append(roi)
				labels.append(0)
				negatives += 1
		else:
			break

		cv2.namedWindow('Region Proposals', cv2.WINDOW_NORMAL)
		cv2.resizeWindow('Region Proposals', 500, 500)
		cv2.namedWindow('Groudtruth', cv2.WINDOW_NORMAL)
		cv2.resizeWindow('Groudtruth', 500, 500)
		cv2.namedWindow('Selected ROIs', cv2.WINDOW_NORMAL)
		cv2.resizeWindow('Selected ROIs', 500, 500)
		cv2.imshow('Region Proposals', region_proposals)
		cv2.imshow('Groudtruth', gt)
		cv2.imshow('Selected ROIs', final_rois)
		cv2.waitKey()

	processing_image+=1

cv2.destroyAllWindows()

images = np.array(images)
labels = np.array(labels)
labels = keras.utils.to_categorical(labels, num_classes=2)
print(images.shape)

train_images, test_images, train_labels, test_labels = train_test_split(images, labels, test_size=0.2)



# Transfer learning using ResNet50 pre-trained with ImageNet
model = ResNet50(include_top=False,weights='imagenet', input_shape = (224,224,3))
last_layer = model.output
x = GlobalAveragePooling2D()(last_layer)
x = Dense(128, activation='relu',name='dense_1')(x)
x = Dropout(0.5)(x)
x = Dense(256, activation='relu',name='dense_2')(x)
x = Dropout(0.5)(x)

# 2 classes (robots and background), more can be added
out = Dense(2,activation='softmax',name='output_layer')(x)

custom_model = Model(inputs=model.input, outputs=out)

for layer in custom_model.layers[:len(model.layers)-10]:
	layer.trainable = False

for l in custom_model.layers:
    print(l.name, l.trainable)

custom_model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])


filepath = 'detection.h5'
checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
custom_model.fit(train_images, train_labels, verbose = 1, epochs=5, validation_data = (test_images, test_labels), batch_size = 4, callbacks = [checkpoint]) 


backend.clear_session()