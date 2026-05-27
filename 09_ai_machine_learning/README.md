# EU_09 – Practical Application of AI

> **Robotics Frameworks (RoF) · FAU Erlangen-Nürnberg · Winter Semester 2025/26**

---

## 📖 Theory Overview

### Why AI for Robotics?
Robots encounter complex perceptual tasks (object recognition, scene understanding) where classical algorithm-based approaches struggle. Trained neural networks can learn features directly from data.

### Convolutional Neural Networks (CNN)
CNNs are the foundation of modern computer vision:

```
Input Image (28×28×1)
      ↓
[Conv2D 32 filters 3×3]  → Feature maps (detects edges, shapes)
      ↓
[MaxPooling 2×2]          → Downsamples (reduces spatial dimensions)
      ↓
[Conv2D 64 filters 3×3]  → Deeper feature maps (detects patterns)
      ↓
[MaxPooling 2×2]
      ↓
[Flatten]                 → Convert 2D feature maps to 1D vector
      ↓
[Dropout 0.5]             → Regularization (prevents overfitting)
      ↓
[Dense 10, softmax]       → Classification output (10 digit classes)
```

### Training Concepts
| Concept | Explanation |
|---|---|
| **Loss function** | Measures prediction error; `categorical_crossentropy` for multi-class |
| **Optimizer** | Algorithm to update weights; `adam` = adaptive learning rate |
| **Epoch** | One full pass through the training data |
| **Batch size** | Number of samples processed before parameter update |
| **Validation set** | Held-out data to monitor overfitting during training |

### Transfer Learning (VGG16)
Instead of training from scratch, use a **pre-trained network** (trained on ImageNet with 1M+ images) and adapt it to a new task:

```
VGG16 (pre-trained on ImageNet, frozen layers)
      ↓
[Flatten]                 → Convert to vector
[Dense 1024, ReLU]        → New custom head
[Dropout 0.5]
[Dense 3, softmax]        → 3 custom classes
```

**Why freeze?** The early layers of VGG16 already detect generic features (edges, textures). Only the last few layers need fine-tuning for domain-specific features.

### YOLO (You Only Look Once) — Real-time Object Detection
YOLO divides the image into a grid and predicts bounding boxes + class probabilities **in a single forward pass**:
- **YOLOv8** (Ultralytics): state-of-the-art, supports tracking (`model.track()`)
- Outputs: bounding box (x1, y1, x2, y2), class label, confidence score
- Threshold: only accept detections with `confidence > 0.4`

```
Camera Frame → YOLOv8 → [bbox, class, confidence] → Draw on frame → Display
```

---

## 📁 File Structure

```
exercise-9-practical-application-of-ai-main/
├── README_EU09.md                  # This file
├── YOLO_example.py                 # Real-time object detection with YOLOv8
├── keras_example.py                # Exercise template: CNN on MNIST (ToDo gaps)
├── keras_example_solution.py       # ✅ Complete CNN solution
├── keras_retrain.py                # Exercise template: Transfer learning (ToDo gaps)
├── keras_retrain_solution.py       # ✅ Complete transfer learning solution
└── yolov8s.pt                      # Pre-trained YOLOv8s model weights (22 MB)
```

---

## 🧠 Code Explanation

### `keras_example_solution.py` — CNN on MNIST

```python
# Build the model (Sequential API)
model = keras.Sequential([
    keras.Input(shape=(28, 28, 1)),
    layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),  # 32 feature maps
    layers.MaxPooling2D(pool_size=(2, 2)),                      # Downsample 2x
    layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),  # 64 feature maps
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Flatten(),                                           # Vectorise
    layers.Dropout(0.5),                                        # 50% dropout
    layers.Dense(10, activation="softmax"),                     # 10 digit classes
])

# Compile
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

# Train (5 epochs, batch 256, 10% validation)
history = model.fit(train_images, train_labels, batch_size=256, epochs=5, validation_split=0.1)

# Evaluate on test set
model.evaluate(test_images, test_labels)
```

**Expected accuracy: ~98-99% on MNIST after 5 epochs.**

### `keras_retrain_solution.py` — Transfer Learning with VGG16

```python
# Load VGG16 without the top classification layer
vgg16_model = VGG16(weights='imagenet', include_top=False, input_shape=(128, 128, 3))

# Freeze all layers EXCEPT the last 4 (fine-tune only the deep features)
for layer in vgg16_model.layers[:-4]:
    layer.trainable = False

# Build new model on top of VGG16
model = keras.Sequential([
    vgg16_model,                          # Pre-trained feature extractor
    layers.Flatten(),
    layers.Dense(1024, activation='relu'), # Custom fully connected layer
    layers.Dropout(0.5),
    layers.Dense(3, activation='softmax'), # 3 custom output classes
])
```

### `YOLO_example.py` — Real-time Object Detection

```python
yolo = YOLO('yolov8s.pt')          # Load pre-trained YOLOv8 small model
cap  = cv2.VideoCapture(0)         # Open webcam

while True:
    ret, frame = cap.read()
    results = yolo.track(frame, stream=True)  # Track objects across frames
    for result in results:
        for box in result.boxes:
            if box.conf[0] > 0.4:             # Only confident detections
                x1, y1, x2, y2 = [int(v) for v in box.xyxy[0]]
                cv2.rectangle(frame, (x1, y1), (x2, y2), colour, 2)
                cv2.putText(frame, f'{class_name} {conf:.2f}', ...)
    cv2.imshow('frame', frame)
```

---

## ▶️ Running the Code

### Install Dependencies
```bash
pip install opencv-python ultralytics tensorflow keras numpy matplotlib
```

### Run YOLO Real-time Detection
```bash
python YOLO_example.py
# → Opens webcam, draws bounding boxes and class labels
# → Press 'q' to quit
```

### Run Keras CNN Training
```bash
# Exercise version (complete the ToDo sections first):
python keras_example.py

# Complete solution:
python keras_example_solution.py
# → Trains CNN on MNIST dataset (~2 min)
# → Plots accuracy and loss curves
```

### Run Transfer Learning
```bash
# Complete solution:
python keras_retrain_solution.py
# → Loads VGG16, prints frozen/trainable layer status
# → Shows combined model architecture summary
```

---

## 📝 Task Summary (from EU_09 PDF)

> **Tasks:**
> 1. Set up the model architecture with Keras (Input → Conv2D → MaxPool → ... → Dense)
> 2. Display the first 9 MNIST images with matplotlib
> 3. Compile with categorical crossentropy + Adam optimizer + accuracy metric
> 4. Evaluate the trained model on the test set
> 5. Load VGG16 and freeze all but the last 4 layers
> 6. Add a new classification head (Flatten → Dense 1024 → Dropout → Dense 3)
> 7. Run YOLOv8 real-time object detection via webcam

---

## 🔗 References
- [Keras/TensorFlow Documentation](https://keras.io/)
- [YOLOv8 Ultralytics](https://docs.ultralytics.com/)
- [MNIST Dataset](http://yann.lecun.com/exdb/mnist/)
- [VGG16 Paper](https://arxiv.org/abs/1409.1556)
- [Transfer Learning Guide](https://keras.io/guides/transfer_learning/)
- [YOLO ROS Wrapper](https://github.com/leggedrobotics/darknet_ros)
