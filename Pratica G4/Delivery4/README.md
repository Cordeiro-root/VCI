# Visão por Computador na Industria - Industrial Computer Vision (Group 04)

### Deliverable 4 &rarr; Edge, contour and object detection

To run a script write the command ``` python *filename* ``` without any extra parameter. It is given, bellow, a brief indication and explanation of the most relevant scripts, the ones not listed bellowed where used to understand and test concepts.

- ``` 1_gradients.py ```

Is applied to a video different types of image gradients. Once ran the script, the type of image gradient is choosen on a Trackbar that indicate the value of each gradient type. Press 'esc'o close to program.


- ``` 2_canny_edge.py ```

Canny edge detection algorithm. After running the script three windows appear, one with the original video, other with Canny edge detection apllied, and a third with trackers assigned to each parameter to be manipulated. Press 'esc' to close to program.
 

- ``` 3_contour_detection.py ```

After running the script three windows appear, one with the original video, other with contor detection apllied, and a third with trackers assigned to each parameter to be manipulated. Press 'esc' to close to program.


-``` 4_ball_lines_detection.py```

The code is design to detect lines and balls. Once ran, it opens a windows with a stram of the video where detection occours if green lines to indicate detected lines and green circles to indicate detected circles. The initial parameters are applied to better detect balls and lines in the video in use but they can be changed on the assigned trackbars. Trackbars with '*parameter*(c)' are the parameters for circle detection and trackbars with '*parameter*(l)' are the parameters for line detection. Press 'esc' to close to program.


-``` 5_template_matching.py, 5_template_matching_video.py ```

Preform template matching, on a image using multiple methods for 5_template_matching.py, and on a video using the cv.TM_CCOEFF method. When using the former, the used method is described on the top of the image, simply press 'esc' to see the next method. 

-``` 6_machine_learning_train.py, 6_machine_learning_test.py ```

Before running these scripts tensorflow alongside with keras have to be installed on a virtual environment. OS and sklearn modules also need to be installed and the RoboCup MSL Dataset available on elearning downloaded. The next is straightforward, 6_macine_learning_train.py needs to be ran first and then run 6_machine_learning_test.py.
