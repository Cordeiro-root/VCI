# Visão por Computador na Industria - Industrial Computer Vision (Group 04)

### Deliverable 5 &rarr; Tracking

The three points requested for this deliverable are fulfilled by the 3 following Python scripts. To be able to run them, it's sufficient to write the command ``` python *filename* ``` without any extra parameter.

- ``` 1_multi_object_tracking.py ```

Tracking of balls and robots in the scene, assigning a label and an ID to each one. We detect objects using color segmentation, then checking the size and the shape to refine the estimation.  Once we have computed a bounding box for each object, we call the method ` CentroidTracker.update(bboxes, True) ` from the [` centroidtracker.py `](https://github.com/Cordeiro-root/VCI/blob/master/Pratica%20G4/Delivery5/centroidtracker.py) library, which we found [here](https://www.pyimagesearch.com/2018/07/23/simple-object-tracking-with-opencv/). This module handles the behaviour of the IDs also when new objects appear or other objects disappear. All these computations are made frame by frame.

- ``` 2_multi_tracker_by_choice.py ```

Here, we used some built-in tracking functions from OpenCV. After running the script, following the prompts appearing in the command line, you can select one or more ROI to track. Unfortunately, due to computational requirements, the more regions of interest you select the slower will be the processing. It could be interesting to see what happens using a GPU.
 
- ``` 3_optical_flow_with_ID.py ```

Eventually, we used the concept of optical flow to track the objects in the scene. Taking the first frame, we apply the same rationale as in the script for the first point to extract the bounding boxes. Then, from these bounding boxes we compute the centroids, and these are what we give to the ` cv.calcOpticalFlowPyrLK(...) ` OpenCV algorithm. This implementation of the Lucas-Kanade algorithm will give us the prediction of the next position for each object for every subsequent frame. However, to take into account new objects entering the scene or other objects not visible anymore, we repeat the initial procedure of object detection once every 10 frames. We assign a label and an ID to each object in the same way as in the first point.

### Things to improve

We were able to make the tracking work both in the first and in the third points, but the precision is not very accurate. We believe that the main problem is in the initial object detection, which should be more effective.