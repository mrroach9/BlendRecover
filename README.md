BlendRecover
============

An algorithm that recovers the original image from a linear blended image of two images, given another original image.
Implemented in Python.

###Dependencies

* python 2.7+
* numpy 1.7+
* opencv 2.4+

###How to use

Specify file names of img A and B in main.py and run. The testing code will blend A and B using alpha = 0.1, 0.2, ..., 0.9, and run recovering algorithm on each (A, tA+(1-t)B) pair and output recovered images (together with blended images). Change whatever parameters you like to see different results.

Image sizes must match, and cannot be too large, otherwise you might encounter memory issues.

###Algorithm

Blending of two images A and B can be represented as C = tA + (1-t)B, while t is the alpha value ranging from 0 to 1. The objective of the algorithm is to estimate t given C and A.

The assumption we made is that feature points of A and B does not always coincident. This covers almost all scenarios that are theoretically solvable (you can never recover from an image blended by a chessbord and its color-reversed version).

Based on the above assumption, we calculate x and y-axis gradient of all 3 channels (RGB) for each image, which gives every pixel a 6-dimension feature for image A and image C (let Axy and Cxy denote the feature vectors at position (x, y)). Filter out all pixels with cos(Axy, Cxy) close to 1 (almost parallel), and set Txy = Axy.Cxy / |Axy|^2 for them. We claim that Txy is close to the real alpha value. 

For all those Txy's, apply 1-D RANSAC algorithm on them which will return an estimated value of alpha (i.e. value of t). Apply B = (C - tA) / (1-t) will recover the image.

###Results

Here are sample estimated alpha results (compared with actual alpha used in blending). Note that the algorithm can recover image B even when it only lies an extremely shallow layer on A.

* Actual alpha = 0.1, estimated alpha = 0.112902712055, inlierRatio = 0.554084356647
* Actual alpha = 0.2, estimated alpha = 0.207447986441, inlierRatio = 0.615470742868
* Actual alpha = 0.3, estimated alpha = 0.300773029393, inlierRatio = 0.610942857143
* Actual alpha = 0.4, estimated alpha = 0.402590938953, inlierRatio = 0.60029606311
* Actual alpha = 0.5, estimated alpha = 0.50318104225, inlierRatio = 0.597439489454
* Actual alpha = 0.6, estimated alpha = 0.601678988569, inlierRatio = 0.59710681059
* Actual alpha = 0.7, estimated alpha = 0.700427572526, inlierRatio = 0.618802192941
* Actual alpha = 0.8, estimated alpha = 0.799603891742, inlierRatio = 0.661073144326
* Actual alpha = 0.9, estimated alpha = 0.899509377766, inlierRatio = 0.754840733064

