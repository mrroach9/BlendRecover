# Known that image C is a mixture of image A and B with some alpha
# value, i.e. C = tA + (1-t)B. Given A and C, estimate t and B.
#
# Author: Wenqi Zhang (MrRoach9)
# License: Apache License v2

import numpy as np
import cv2

# Adjustable parameters

# Before RANSAC, eliminate pixels that has too small cosine between
# blended image feature and original image A feature. This will 
# significantly improve precision and reduce time.
COS_ELIMINATE = 0.99

# Radius for 1-D RANSAC algorithm on estimating alpha value. Values
# fall in the interval [c - r, c + r] will be considered inliers.
RANSAC_RADIUS = 0.05


# calculate x and y directional gradient of the image in 3 channels
# respectively, assemble the result as a 6-dimensional feature
# for each pixel.
def calcGradient(img):
    grad = np.zeros([img.shape[0], img.shape[1], 6], np.float32);
    for i in range(3):
        grad[:, :, 2 * i] = cv2.Sobel(img[:, :, i], cv2.CV_16S, 0, 1)
        grad[:, :, 2 * i + 1] = cv2.Sobel(img[:, :, i], cv2.CV_16S, 1, 0)
    return grad / 255.0

# gradA is the 6 dimensional gradient matrix of A
# gradC is the 6 dimensional gradient matrix of C
def estimateAlpha(gradA, gradC):
    dotProd = np.sum(gradA * gradC, 2)
    lenA = np.sqrt(np.sum(gradA * gradA, 2)) + 1e-6
    lenC = np.sqrt(np.sum(gradC * gradC, 2)) + 1e-6
    cos = dotProd / (lenA * lenC);

    alpha = dotProd / (lenA * lenA)
    alpha[cos < COS_ELIMINATE] = -1
    alphaList = np.reshape(alpha, [-1])
    alphaList = alphaList[alphaList >= 0]
    alphaList = alphaList[alphaList <= 1]
    alphaList = np.sort(alphaList)
    length = len(alphaList)

    rad = RANSAC_RADIUS
    maxInlier = 0
    aEst = 0
    print length, alphaList
    right = 0
    for left in range(length):
        while right < length and alphaList[right] - alphaList[left] < 2 * rad:
            right += 1
        if right - left > maxInlier:
            maxInlier = right - left
            aEst = np.sum(alphaList[left : right]) / float(maxInlier)
    return aEst, maxInlier / float(alphaList.shape[0])

def loadImg(filename1, filename2):
    img1 = cv2.imread(filename1)
    img2 = cv2.imread(filename2)
    if img1 is None or img2 is None:
        return None, None
    if img1.shape[0] != img2.shape[0] or img1.shape[1] != img2.shape[1]:
        return None, None
    if img1.shape[2] != 3 or img2.shape[2] != 3:
        return None, None
    return img1, img2

def blendImgForTest(imgA, imgB, alpha):
    return imgA * alpha + imgB * (1 - alpha)

if __name__ == '__main__':
    imgA, imgB = loadImg("img1.jpg", "img2.jpg")
    for alphaLevel in range(1, 10):
        print 'Processing alphaLevel = {0}'.format(alphaLevel)
        alpha = alphaLevel / 10.0
        imgC = blendImgForTest(imgA, imgB, alpha)
        cv2.imwrite('img3_{0}_blend.jpg'.format(alphaLevel), imgC)
        gradA = calcGradient(imgA)
        gradC = calcGradient(imgC)
        alphaEst, inlierRatio = estimateAlpha(gradA, gradC)
        print 'Actual alpha = {0}, estimated alpha = {1}, inlierRatio = {2}'\
              .format(alpha, alphaEst, inlierRatio)
        imgBEst = (imgC - alphaEst * imgA) / (1 - alphaEst)
        cv2.imwrite('img2_{0}_est.jpg'.format(alphaLevel), imgBEst)
