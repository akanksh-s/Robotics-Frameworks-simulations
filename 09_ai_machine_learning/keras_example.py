#!/usr/bin/python3

# Import necessary libraries
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np
import tensorflow as tf
import keras
from keras import layers
import matplotlib.pyplot as plt


# Create a sequential model using Keras
# ToDo

'''
# ToDo: Add layers to the model
# Input layer with shape (28, 28, 1)
# Convolutional layer with 32 3x3 filters and ReLU activation
# Max pooling layer with pool size (2, 2)
# Convolutional layer with 64 3x3 filters and ReLU activation
# Max pooling layer with pool size (2, 2)
# Flatten layer to convert the 2D matrix data to a vector
# Dropout layer to prevent overfitting
# Fully connected layer with 10 units and softmax activation

# Display a summary of the model architecture
model.summary()

# Load the MNIST dataset and split it into training and testing sets
(train_images, train_labels), (test_images, test_labels) = keras.datasets.mnist.load_data()

# ToDo: Display the first 9 images from the training set using matplotlib

# Preprocess the image data by scaling pixel values to the range [0, 1] and adding a channel dimension
train_images = train_images.astype("float32")/255
test_images = test_images.astype("float32")/255
train_images = np.expand_dims(train_images, -1)
test_images = np.expand_dims(test_images, -1)

# One-hot encode the labels
train_labels = keras.utils.to_categorical(train_labels, 10)
test_labels = keras.utils.to_categorical(test_labels, 10)

# ToDo: Compile the model with categorical crossentropy loss, Adam optimizer, and accuracy metric

# Train the model on the training data, with validation split and specified batch size and epochs
history = model.fit(train_images, train_labels, batch_size=256, epochs=5, validation_split=0.1)

# ToDo: Evaluate the model on the test data

# Display keys of the history object (contains training and validation metrics)
print(history.history.keys())

# Plot the training and validation accuracy over epochs
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# Plot the training and validation loss over epochs
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
'''