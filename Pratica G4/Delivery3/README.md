# Visão por Computador na Industria - Industrial Computer Vision (Group 04)

### Deliverable 3 &rarr; Color segmentation, object detection on grayscale image.

To run a script write the command ``` python *filename* ``` without any extra parameter. It is given, bellow, a brief indication and explanation of the most relevant scripts, the ones not listed bellowed where used to understand and test concepts.

- ``` 1_paint.py, 1_trackbar ```

1_paint.py demonstrate the use of cv.setMouseCallback() by drawing. Is possible to draw a rectangle by draging the mouse or use the mouse as a brush. To switch between options press 'm', ans to quit press 'esc'.
1_trackbar demonstrate the use of cv.getTrackbarPos() and cv.createTrackbar()) by painting a window with the color corresponding to the RGB values of the trackbar. To change the color simply slide a trackbar.

- ``` 2_trackbars_segmentation.py```

Double click to open the image, slide parameters trackbar to adjust the values of the desired colors. The values of import colors of CAMBADA soccer field are indicated in the window.

- ``` 3_object_detection.py ```

Object detection on grayscale images. After running the script, double click on the indicated area to open the video, than choose the object to be detected by seting the assign trackbar to '1', multiple objects can be tracked 

