import os
from PIL import Image
import tensorflow as tf
from tensorflow import keras
import numpy as np
import cv2
import random
import time
import keras_tuner as kt

LOG_DIR = f"{int(time.time())}"
path1 = "D:/ResetEfficiency/"
bs = 25
epoch_num = 14
max_images = 1848
label = sorted(os.listdir(path1 + "nn_images/bt_identification/train_images/unanalyzed"))
dataset = []
weights = {
    0: 0.65,
    1: 0.35
}


def make_model():
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Rescaling(scale=1./255))
    for i in range(3):
        model.add(tf.keras.layers.Dense(32, activation=tf.nn.relu))
    model.add(tf.keras.layers.Dense(2, activation=tf.nn.softmax))
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.0001),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model


def make_dataset(type):
    dataset = []
    X = []
    Y = []

    for image_label in label:
        if type == "bt_images" or image_label != "weak-learners":
        #if image_label == "bt":
            images = os.listdir(path1 + "nn_images/bt_identification/" + type + "/unanalyzed/" + image_label)
            count = 0
            categorical_max_images = max_images/4
            if image_label == "bt":
                categorical_max_images = max_images/2
            if len(images) > categorical_max_images:
                for i in range(len(images)-int(categorical_max_images)):
                    images.pop(random.randrange(0, len(images)))
            for image in images:
                if count < categorical_max_images:
                    count += 1
                    error_flag = False
                    if image.endswith('.png'):
                        try:
                            img = Image.open(path1 + "nn_images/bt_identification/" + type + "/unanalyzed/" + image_label + "/" + image)
                            img.verify()
                        except (IOError, SyntaxError) as e:
                            error_flag = True
                        if not error_flag:
                            img = cv2.imread(path1 + "nn_images/bt_identification/" + type + "/unanalyzed/" + image_label + "/" + image)
                            if image_label == "bt":
                                dataset.append((img, "bt"))
                            else:
                                dataset.append((img, "non-bt"))

    for input1, image_label in dataset:
        X.append(input1)
        Y.append(label.index(image_label))

    X = np.array(X)
    Y = np.array(Y)

    return (X, Y)


def train_model():
    model = make_model()
    if len(os.listdir(path1 + "models")) == 0:
        make_model()
    else:
        model = tf.keras.models.load_model(path1 + 'models/model1')
    X_train, y_train, = make_dataset("train_images")
    model.fit(X_train, y_train, epochs=epoch_num, class_weight=weights, batch_size=bs)
    model.save(path1 + 'models/model1')


def evaluate_model():
    model = tf.keras.models.load_model(path1 + 'models/model1')
    X_test, y_test, = make_dataset("test_images")
    model.evaluate(X_test, y_test, batch_size=bs)


#X_train, y_train, = make_dataset("bt_images")
#X_test, y_test, = make_dataset("test_images")
#tuner = kt.RandomSearch(make_model, objective="val_accuracy", max_trials=100, executions_per_trial=2, directory=LOG_DIR)
#tuner.search(x=X_train, y=y_train, epochs=epoch_num, batch_size=bs, validation_data=(X_test, y_test))

train_model()
