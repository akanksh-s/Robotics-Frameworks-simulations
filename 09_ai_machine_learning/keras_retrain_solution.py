#!/usr/bin/python3

# Import necessary libraries
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import numpy as np
import tensorflow as tf
import keras
from keras import layers
from keras.applications import VGG16

# Load the pre-trained VGG16 model with weights from ImageNet
vgg16_model = VGG16(weights='imagenet', include_top=False, input_shape=(128, 128, 3))

# Freeze the layers except the last 4 layers to prevent them from being trained
for layer in vgg16_model.layers[:-4]:
    layer.trainable = False

# Print the trainable status of each layer in the VGG16 model
for layer in vgg16_model.layers:
    print(layer, layer.trainable)

# Display a summary of the VGG16 model architecture
vgg16_model.summary()

# Create a new sequential model and add the pre-trained VGG16 model as the first layer
model = keras.Sequential()
model.add(vgg16_model)

# Flatten the output of the VGG16 model
model.add(layers.Flatten())

# Add a fully connected layer with 1024 neurons and ReLU activation
model.add(layers.Dense(1024, activation='relu'))

# Add a dropout layer with a dropout rate of 0.5 to prevent overfitting
model.add(layers.Dropout(0.5))

# Add the final output layer with 3 neurons and softmax activation for classification
model.add(layers.Dense(3, activation='softmax'))

# Display a summary of the complete model architecture
model.summary()
