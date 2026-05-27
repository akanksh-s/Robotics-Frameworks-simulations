# EU_05 – Practical Application of Computer Vision

> **Robotics Frameworks (RoF) · FAU Erlangen-Nürnberg · Winter Semester 2025/26**

---

## 📖 Theory Overview

### OpenCV and Image Processing
**OpenCV** (Open Source Computer Vision Library) is the industry-standard library for real-time image processing. In ROS2 robotics, it is used to process camera frames before passing them to detection algorithms.

### Color Spaces
Cameras capture images in **BGR** (Blue-Green-Red, OpenCV default) color order. Converting to other color spaces enables different types of analysis:

| Color Space | Function | Use Case |
|---|---|---|
| BGR | Default (OpenCV) | Raw camera output |
| RGB | `cv2.COLOR_BGR2RGB` | Display with matplotlib |
| Grayscale | `cv2.COLOR_BGR2GRAY` | Edge detection, thresholding |
| HSV | `cv2.COLOR_BGR2HSV` | Color-based object segmentation |

### Binary Thresholding
Converts a grayscale image into a binary (black/white) image:
```python
(thresh, binary) = cv2.threshold(gray, threshold_value, max_value, cv2.THRESH_BINARY)
# Pixels > threshold → max_value (white = 255)
# Pixels ≤ threshold → 0 (black)
```

### Smoothing and Blurring
Removes noise before edge detection:

| Method | Function | Characteristics |
|---|---|---|
| Average (Box) | `cv2.blur(img, (kW, kH))` | Simple mean of neighborhood |
| Gaussian | `cv2.GaussianBlur(img, (kW, kH), 0)` | Weighted by Gaussian curve, preserves edges better |
| Median | `cv2.medianBlur(img, k)` | Very effective for salt-and-pepper noise |

*Larger kernel → more blurring.*

### Canny Edge Detection
Finds edges via gradient magnitude and non-maximum suppression:
```python
edges = cv2.Canny(image, low_threshold, high_threshold)
# Typically: low = 50, high = 200
```
Steps: Gaussian blur → Gradient computation → Non-max suppression → Double threshold → Edge tracking

### Perspective Transformation (Homography)
Corrects for camera tilt/angle by mapping image corners to a frontal view:
```python
M = cv2.getPerspectiveTransform(src_points, dst_points)   # 4-point correspondence
result = cv2.warpPerspective(image, M, (width, height))
```

---

## 📁 File Structure

```
exercise-5-practical-application-of-cv-main/
├── README_EU05.md                      # This file
├── robots.png                          # Test image for image_processing tasks
├── paper.jpeg                          # Test image for perspective transformation
├── coca_cola.jpg                       # Additional test image
├── image_processing.py                 # Exercise template (ToDo markers)
├── image_processing_solution.py        # ✅ Complete solution
├── perspective_transformation.py       # Exercise template (ToDo markers)
└── perspective_transformation_solution.py  # ✅ Complete solution
```

---

## 🧠 Code Explanation

### `image_processing_solution.py` — Step-by-Step

```python
# 1. Read image (BGR format)
image = cv2.imread('robots.png')

# 2. Convert BGR → RGB (for matplotlib display)
image_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 3. Convert to grayscale
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 4. Binary threshold: pixels > 175 → white, else black
(thresh, image_binary) = cv2.threshold(image_gray, 175, 255, cv2.THRESH_BINARY)

# 5. Blurring comparison: Average, Gaussian, Median
kernel_sizes = [(3, 3), (9, 9), (15, 15)]
for (x, y) in kernel_sizes:
    average = cv2.blur(image_smoothing, (x, y))
    gaussian = cv2.GaussianBlur(image_smoothing, (x, y), 0)
for k in (3, 9, 15):
    median = cv2.medianBlur(image_smoothing, k)

# 6. Canny edge detection
edges_canny = cv2.Canny(image_canny, 50, 200)
```

### `perspective_transformation_solution.py` — Key Code

```python
# 4 corner points of the paper in the original tilted photo
# (upper-left, upper-right, lower-left, lower-right)
points_before = np.float32([[92, 24], [220, 73], [26, 98], [172, 174]])

# Target rectangle (full image size after transform)
points_after = np.float32([[0, 0], [paper.shape[1], 0],
                            [0, paper.shape[0]], [paper.shape[1], paper.shape[0]]])

# Compute the 3×3 homography matrix
M = cv2.getPerspectiveTransform(points_before, points_after)

# Apply the transformation
paper_transformed = cv2.warpPerspective(paper, M, (paper.shape[1], paper.shape[0]))
```

---

## ▶️ Running the Code

```bash
# Install dependencies
pip install opencv-python matplotlib numpy

# Run the image processing exercise
cd exercise-5-practical-application-of-cv-main
python image_processing_solution.py

# Run the perspective transformation exercise
python perspective_transformation_solution.py
```

> **Tip:** In the perspective transformation script, click on the corners of the paper to find your own `points_before` coordinates (the mouse callback prints x,y).

---

## 📝 Task Summary (from EU_05 PDF)

> **Tasks:**
> 1. **Color Conversion** — Load `robots.png`, convert to RGB and Grayscale, display both
> 2. **Thresholding** — Apply binary threshold (value 175) to the grayscale image
> 3. **Blurring** — Apply Average, Gaussian and Median blur with kernels (3,3), (9,9), (15,15)
> 4. **Canny Edge Detection** — Detect edges with thresholds 50 and 200; overlay with matplotlib
> 5. **Perspective Transform** — Correct the perspective of `paper.jpeg` by identifying the 4 corners

---

## 🔗 References
- [OpenCV Python Tutorials](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [Canny Edge Detection](https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html)
- [Perspective Transform](https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html#gaf73673a7e8e18ec6963e3774e6a94b87)
