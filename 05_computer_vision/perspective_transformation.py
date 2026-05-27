import cv2
from operator import itemgetter
from glob import glob
import matplotlib.pyplot as plt
import numpy as np

paper = cv2.imread('paper.jpeg')
cv2.imshow("Original Image", paper)
cv2.waitKey(0)

'''
# coordinates that need to be perspective transformed
# (upper left, upper right, lower left, lower right)
points_before = # ToDo

# size of the perspective transformed image
points_after = # ToDo

# mark the points for the perspective transformation in the original image
for k in points_before:
    # ToDo

# get the projection matrix M
M = # ToDo

# apply perspective transformation to the original image
paper_transformed = # ToDo

cv2.imshow("Original Image", paper)
cv2.imshow("Transformed Image", paper_transformed)
cv2.waitKey(0)
cv2.destroyAllWindows()'''