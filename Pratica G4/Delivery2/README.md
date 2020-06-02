# Visão por Computador na Industria - Industrial Computer Vision (Group 04)

### Deliverable 2; Transforme color spaces HSV, YUV and GRAY, calculate Histograms and equalization, and Gaussian and blur filters

The second deliverable, we transform the acquired images to other color spaces, YUV, HSV and GRAY, calculate histograms in real time such as histogram equalization, and we aplly the gaussian and blur filters with diferent kernels.

- ``` 1-rgb-hsv-gray.py ``` and ``` 1-rgb-hsv-video.py ``` 

Here we can see the results off the transfoming color spaces, using an image, and while capturing video.

- ``` 2-histograms.py ``` 

Here we have the results off the histograms in real time, for all the transformed images, HSV, YUV etc..., we can see that it gets a little slow, because it is processing various histograms at the same time.

- ``` 3-hist_equalization.py ``` 

With this code we can see the equalization on grayscale in real time, and the respective histogram.

- ``` 4-gauss-blur-video.py ```

Finaly we can explore different filters, like Gaussian, Bilateral and Median.

### Other files
We also have a lot off test files, where we try the various functions and tutorials before we reach the final result. 