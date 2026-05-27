import cv2
from operator import itemgetter
from glob import glob
import matplotlib.pyplot as plt
import numpy as np

# Function on clicking in the original image to print the coordinates of the corners for line 19
def on_click(event, x, y, falgs, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print('x = %d, y = %d'%(x, y)) 

paper = cv2.imread('paper.jpeg')
cv2.imshow("Original Image", paper)
cv2.setMouseCallback("Original Image", on_click)
cv2.waitKey(0)

# coordinates that need to be perspective transformed
# (upper left, upper right, lower left, lower right)
points_before = np.float32([[92, 24], [220, 73], [26, 98], [172, 174]])

# size of the perspective transformed image
points_after = np.float32([[0, 0], [paper.shape[1], 0], [0, paper.shape[0]], [paper.shape[1], paper.shape[0]]])

# mark the points for the perspective transformation in the original image
for k in points_before:
    cv2.circle(paper, (int(k[0]), int(k[1])), 5, (0, 255, 0), -1)

# get the projection matrix M
M = cv2.getPerspectiveTransform(points_before, points_after)

# apply perspective transformation to the original image
paper_transformed = cv2.warpPerspective(paper, M, (paper.shape[1], paper.shape[0]))

cv2.imshow("Original Image", paper)
cv2.imshow("Transformed Image", paper_transformed)
cv2.waitKey(0)
cv2.destroyAllWindows()