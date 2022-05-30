import os
from PIL import Image
import tensorflow as tf
import numpy as np
import cv2
import math
import pygsheets
import pandas as pd
import subprocess
import re
from pathlib import Path
import datetime
from datetime import timedelta
import gc
import mmap


path1 = "D:/ResetEfficiency/"

dsize = (1920, 1080)
max_images = 2000
bt_threshold = 0.9
username_list = ["makattak11", "7rowl", "semperzz", "silverrruns"]
FPS_list = [50, 60, 60, 60]
timezone_list = [timedelta(hours=-5), timedelta(hours=2), timedelta(hours=-6), timedelta(hours=-8)]
uses_new_tracker = [True, False, True, False]
max_videos_per_user = 10
model = tf.keras.models.load_model(path1 + 'models/model1')
user_index = -1


def download_vod(url, name):
    subprocess.run(f'twitch-dl download {url} -f mp4 -q source -o {path1}vods/{name}.mp4')


def frames_to_time(list1, start_time):
    start_datetime = datetime.datetime(year=int(start_time[0:4]),
                                       month=int(start_time[5:7]),
                                       day=int(start_time[8:10]),
                                       hour=int(start_time[11:13]),
                                       minute=int(start_time[14:16]),
                                       second=int(start_time[17:19]))
    for i in range(len(list1)):
        list1[i] = str(list1[i])
        list1[i] = math.floor(int(list1[i][:len(list1[i])-4]) / FPS_list[user_index])
        seconds = list1[i]
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        timestamp = timedelta(hours=hour, minutes=minutes, seconds=seconds)
        date_and_time = start_datetime + timezone_list[user_index] + timestamp
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
        if cur_frame % FPS_list[user_index]:
            continue

        _, frame = video.retrieve()
        frame = cv2.resize(frame, dsize)
        frame = frame[200:880, 630:1290]
        frames.append(cur_frame)
        cv2.imwrite(path1 + "frames/" + str(cur_frame) + ".png", frame)
        cv2.imshow('window', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

    return frames


def make_dataset():
    dataset = []
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
                    dataset.append((img, image))
                os.remove(path1 + "frames/" + image)

    for input1, input2 in dataset:
        X.append(input1)
        Y.append(input2)

    X = np.array(X)

    return (X, Y)

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
    bt_timestamps = frames_to_time(bt_timestamps, start_time)


    return bt_timestamps


def write_to_gsheets(sheetname, vodpath, start_time):
    gc_sheets = pygsheets.authorize(service_file=path1 + "credentials.json")
    sh = gc_sheets.open(sheetname)
    wks = sh[1]
    column_num = 38
    if uses_new_tracker[user_index]:
        column_num = 41
    bt_timestamps = get_timestamps(vodpath, start_time)
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
                    wks.update_value((i+2, column_num), str(bt_timestamp))
                bt_timestamps.remove(bt_timestamp)
                flag = True


def get_twitch_id(username):
    run = subprocess.run(f"twitch api get users -q login={username}", capture_output=True)
    x = str(run.stdout.decode())
    id = x[(x.find("id") + 6):(x.find("login") - 10)]
    id = int(id)

    return id


def get_streams_info(usernames):
    local_username_list = []
    links = []
    start_times = []
    for username in usernames:
        id = get_twitch_id(username)
        run = subprocess.run(f"twitch api get /videos -q first={max_videos_per_user} -q type=archive -q user_id={id}", capture_output=True)
        x = str(run.stdout.decode())
        links_temp = re.findall("https://www.twitch.tv/videos/\d\d\d\d\d\d\d\d\d\d", x)
        links = links + links_temp

        for i in range(len(x)):
            if x[i:(i + 10)] == "created_at":
                start_times.append((x[(i + 14):(i + 33)]).replace("T", " "))
                local_username_list.append(username)
    return local_username_list, links, start_times


def download_all_vods():
    usernames, links, start_times = get_streams_info(username_list)
    for i in range(len(links)):
        download_vod(links[i], str(i).zfill(4) + usernames[i])
        vodInfo = (usernames[i], links[i], start_times[i], str(i).zfill(4))
        with open('D:/ResetEfficiency/vodInfo.txt', 'a') as f:
            for item in list(vodInfo):
                f.writelines(item + '\n')
            f.writelines('\n')
        for dir in Path('C:/Users/thoma/AppData/Local/Temp/twitch-dl').glob('*'):
            for file in Path((str(dir) + '/chunked')).glob('*'):
                os.remove(file)
    return usernames, start_times


def analyze_all_vods():
    global user_index
    #usernames, start_times = download_all_vods()
    usernames = []
    start_times = []
    total_lines = 0
    with open('D:/ResetEfficiency/vodInfo.txt', "r+") as vodInfo:
        mm = mmap.mmap(vodInfo.fileno(), 0)
        while mm.readline():
            total_lines += 1
        for i in range(total_lines):
            line = vodInfo.readline()
            line = line.replace('\n', '')
            if i % 5 == 0:
                usernames.append(line)
            if i % 5 == 2:
                start_times.append(line)
    count3 = 0
    for vodpath in Path(path1 + "vods").glob("*.mp4"):
        parts = list(vodpath.parts)
        vod = parts[len(parts) - 1]
        for i in range(len(username_list)):
            if username_list[i] in vod:
                user_index = i
        vod_num = int(vod[0:4])
        write_to_gsheets(usernames[count3], vodpath, start_times[vod_num])
        count3 += 1


analyze_all_vods()
