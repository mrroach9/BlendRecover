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

* Actual alpha = 0.1, estimated alpha = 0.117798553914, inlierRatio = 0.35737527115
* Actual alpha = 0.2, estimated alpha = 0.209966807838, inlierRatio = 0.480980012895
* Actual alpha = 0.3, estimated alpha = 0.308397650996, inlierRatio = 0.527066649162
* Actual alpha = 0.4, estimated alpha = 0.406832766168, inlierRatio = 0.548780178213
* Actual alpha = 0.5, estimated alpha = 0.499385442547, inlierRatio = 0.562458120261
* Actual alpha = 0.6, estimated alpha = 0.597386102773, inlierRatio = 0.536343332486
* Actual alpha = 0.7, estimated alpha = 0.699549712642, inlierRatio = 0.529790000717
* Actual alpha = 0.8, estimated alpha = 0.799380876813, inlierRatio = 0.550911923747
* Actual alpha = 0.9, estimated alpha = 0.898431057173, inlierRatio = 0.614390749206

Note that the above results are recovered from JPEG-saved blending image, which considered percision loss from float-integer conversion and JPEG-compression. If we blend in memory and test recovering, it would give better results.
