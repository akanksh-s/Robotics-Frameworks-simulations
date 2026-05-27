# Importing opencv
import cv2

# Importing matplotlib.pyplot
import matplotlib.pyplot as plt

# Reading the image
image = cv2.imread('robots.png')
cv2.imshow('Original Image', image)

# Converting into RGB color space
image_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Displaying the original image
cv2.imshow('RGB Image', image_RGB)

# Converting into grayscale
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Displaying the converted image
cv2.imshow('Grayscale Image', image_gray)

# Converting to binary image using thresholding
(thresh, image_binary) = cv2.threshold(image_gray, 175, 255, cv2.THRESH_BINARY)

# Displaying binary image
cv2.imshow('Binary Image', image_binary)

cv2.waitKey(0)
cv2.destroyAllWindows()


### Reading the image in grayscale mode by setting the flag as 0 ###
img = cv2.imread('robots.png', 0)
(thresh, img_binary) = cv2.threshold(img, 175, 255, cv2.THRESH_BINARY)

# Displaying original grayscale image and binary image
cv2.imshow('Original Image', img)
cv2.imshow('Binary Image', img_binary)

cv2.waitKey(0)
cv2.destroyAllWindows()


### Smoothing and Blurring with OpenCV ###
image_smoothing = cv2.imread('robots.png')
cv2.imshow("Original Image", image_smoothing)
# define different kernel sizes to evaluate the relationship between kernel size and degree of blurring
kernel_sizes = [(3, 3), (9 , 9), (15, 15)]

# loop over the different kernel sizes
for (x, y) in kernel_sizes:
    # apply mean value filter
    image_average_blurred = cv2.blur(image_smoothing, (x, y))
    # show the output image
    cv2.imshow("Average Blurred Image ({}, {})".format(x, y), image_average_blurred)
    cv2.waitKey(0)
cv2.destroyAllWindows()


cv2.imshow("Original Image", image_smoothing)
# loop over the different kernel sizes again
for (x, y) in kernel_sizes:
    # apply gaussian blur filter
    image_gaussian_blur = cv2.GaussianBlur(image_smoothing, (x, y), 0)
    # show the output image
    cv2.imshow("Gaussian Blurred Image ({}, {})".format(x, y), image_gaussian_blur)
    cv2.waitKey(0)
cv2.destroyAllWindows()


cv2.imshow("Original Image", image_smoothing)
# loop over the different kernel sizes again
for k in (3, 9, 15):
    # apply median blur filter
    image_median_blur = cv2.medianBlur(image_smoothing, k)
    # show the output image
    cv2.imshow("Median Blurred Image {}".format(k), image_median_blur)
    cv2.waitKey(0)
cv2.destroyAllWindows()


### Detecting edges with the canny algorithm ###
image_canny = cv2.imread('robots.png')
edges_canny = cv2.Canny(image_canny, 50, 200)

plt.subplot(121),plt.imshow(image_canny) 
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges_canny, cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
plt.show()