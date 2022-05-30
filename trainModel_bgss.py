import os
from PIL import Image
import tensorflow as tf
from tensorflow import keras
import numpy as np
import cv2
import random
import time
import keras_tuner as kt
import pygsheets

LOG_DIR = f"{int(time.time())}"
path1 = "D:/ResetEfficiency/"
bs = 25
epoch_num = 14
max_images = 1848
dataset = []



def make_model(output_neurons):
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Rescaling(scale=1./255))
    for i in range(3):
        model.add(tf.keras.layers.Dense(32, activation=tf.nn.relu))
    model.add(tf.keras.layers.Dense(output_neurons, activation=tf.nn.softmax))
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.0001),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model


def make_dataset(type):
    dataset = []
    X = []
    Y = []
    images = os.listdir(path1 + "nn_images/spawn_image_classification/" + type + "/unanalyzed")
    for image in images:
        error_flag = False
        if image.endswith('.png'):
            try:
                img = Image.open(path1 + "nn_images/bt_identification/" + type + "/unanalyzed/" + image)
                img.verify()
            except (IOError, SyntaxError) as e:
                error_flag = True
            if not error_flag:
                img = cv2.imread(path1 + "nn_images/bt_identification/" + type + "/unanalyzed/" + image)



def train_models():
    modelOcean = make_model(5)
    modelTrees = make_model(2)
    modelBeachType = make_model(3)
    X_train, ocean_train, trees_train, beachType_train = make_dataset("train_images")
    X_test, ocean_test, trees_test, beachType_test = make_dataset("test_images")
    classifications = [{'model': modelOcean, 'training_labels': ocean_train, 'testing_labels': ocean_test, 'name': 'modelOcean'},
                       {'model': modelTrees, 'training_labels': trees_train, 'testing_labels': trees_test, 'name': 'modelTrees'},
                       {'model': modelBeachType, 'training_labels': beachType_train, 'testing_labels': beachType_test, 'name': 'modelBeachType'}]
    for i in range(len(classifications)):
        model = classifications[i]['model']
        training_labels = classifications[i]['training_labels']
        testing_labels = classifications[i]['testing_labels']
        name = classifications[i]['name']
        model.fit(X_train, training_labels, epochs=epoch_num)
        model.evaluate(X_test, testing_labels)
        model.save(path1 + 'models/' + name)
