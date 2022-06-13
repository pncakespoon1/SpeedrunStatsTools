import os
from PIL import Image
import tensorflow as tf
import numpy as np
import cv2
import math
import pygsheets
import datetime
from datetime import timedelta
import gc
import json


path1 = "D:/ResetEfficiency/"
dsize = (1920, 1080)
max_images = 2000
bt_threshold = 0.9
jsonFile1 = open(path1 + "runners.json")
runners = json.load(jsonFile1)
jsonFile3 = open(path1 + "arguments.json")
arguments = json.load(jsonFile3)
model = tf.keras.models.load_model(path1 + 'models/model1')
user_index = arguments['user_index']
gc.enable()


def frames_to_time(list1, start_time):
    start_datetime = datetime.datetime(year=int(start_time[0:4]),
                                       month=int(start_time[5:7]),
                                       day=int(start_time[8:10]),
                                       hour=int(start_time[11:13]),
                                       minute=int(start_time[14:16]),
                                       second=int(start_time[17:19]))
    for i in range(len(list1)):
        list1[i] = str(list1[i])
        list1[i] = math.floor(int(list1[i][:len(list1[i])-4]) / runners[user_index]['fps'])
        seconds = list1[i]
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        timestamp = timedelta(hours=hour, minutes=minutes, seconds=seconds)
        date_and_time = start_datetime + timedelta(hours=runners[user_index]['timezone']) + timestamp + timedelta(seconds=15)
        list1[i] = date_and_time

    return list1


def download_frames(file):
    frames = []
    cur_frame = 0
    video = cv2.VideoCapture(str(file))
    while video.isOpened():
        cur_frame += 1
        if not video.grab():
            break
        if cur_frame % runners[user_index]['fps']:
            continue

        _, frame = video.retrieve()
        frame = cv2.resize(frame, dsize)
        frame = frame[200:880, 630:1290]
        frames.append(cur_frame)
        cv2.imwrite(path1 + "frames/" + str(cur_frame) + ".png", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    video.release()

    return frames


def make_dataset():
    X = []
    Y = []
    images = os.listdir(path1 + "frames")
    count1 = 0
    for image in images:
        if count1 < max_images:
            count1 += 1
            error_flag = False
            if image.endswith('.png'):
                try:
                    img = Image.open(path1 + "frames" + "/" + image)
                    img.verify()
                except (IOError, SyntaxError) as e:
                    error_flag = True
                if not error_flag:
                    img = cv2.imread(path1 + "frames" + "/" + image)
                    X.append(img)
                    Y.append(image)
            os.remove(path1 + "frames" + "/" + image)
    X = np.array(X)
    return X, Y


def get_timestamps(vodpath, start_time):
    download_frames(vodpath)
    bt_timestamps = []
    while len(os.listdir(path1 + "frames")) != 0:
        gc.collect()
        count2 = 0
        image_data, timestamps = make_dataset()
        predictions = model.predict(image_data)
        for i in range(len(predictions)):
            if predictions[i][0] > bt_threshold:
                bt_timestamps.append(timestamps[count2])
            count2 += 1
        del predictions
    bt_timestamps = frames_to_time(bt_timestamps, start_time)


    return bt_timestamps


def write_to_gsheets(sheetnames, vodpath, start_time):
    gc_sheets = pygsheets.authorize(service_file=path1 + "credentials.json")
    bt_timestamps = get_timestamps(vodpath, start_time)
    for image in os.listdir(path1 + 'frames'):
        os.remove(path1 + "frames" + "/" + image)
    for sheetname in sheetnames:
        sh = gc_sheets.open(sheetname)
        wks = sh[1]
        column_num = 38
        if runners[user_index]['tracker_versions'][sheetnames.index(sheetname)] == 2:
            column_num = 41
        if runners[user_index]['tracker_versions'][sheetnames.index(sheetname)] == 3:
            column_num = 31
        tracker_timestamps = wks.get_col(col=1, returnas='matrix', include_tailing_empty=False)
        for i in range(1, len(tracker_timestamps) - 1):
            flag = False
            tracker_timestamp_lower = str(tracker_timestamps[i + 1])
            tracker_timestamp_lower_datetime = datetime.datetime(year=int(tracker_timestamp_lower[0:4]),
                                                                 month=int(tracker_timestamp_lower[5:7]),
                                                                 day=int(tracker_timestamp_lower[8:10]),
                                                                 hour=int(tracker_timestamp_lower[11:13]),
                                                                 minute=int(tracker_timestamp_lower[14:16]),
                                                                 second=int(tracker_timestamp_lower[17:19])
                                                                 )
            tracker_timestamp_upper = str(tracker_timestamps[i])
            tracker_timestamp_upper_datetime = datetime.datetime(year=int(tracker_timestamp_upper[0:4]),
                                                                 month=int(tracker_timestamp_upper[5:7]),
                                                                 day=int(tracker_timestamp_upper[8:10]),
                                                                 hour=int(tracker_timestamp_upper[11:13]),
                                                                 minute=int(tracker_timestamp_upper[14:16]),
                                                                 second=int(tracker_timestamp_upper[17:19])
                                                                 )
            for bt_timestamp in bt_timestamps:
                if tracker_timestamp_lower_datetime < bt_timestamp < tracker_timestamp_upper_datetime:
                    if not flag:
                        wks.update_value((i+1, column_num), str(bt_timestamp))
                    bt_timestamps.remove(bt_timestamp)
                    flag = True


write_to_gsheets(arguments['sheetnames'], arguments['vodpath'], arguments['start_time'])
