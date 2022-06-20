import os
import subprocess
from pathlib import Path
import gc
import mmap
import json


path1 = "D:/ResetEfficiency/"
user_index = -1
jsonFile1 = open(path1 + "runners.json")
runners = json.load(jsonFile1)
jsonFile2 = open(path1 + "downloaded_vod_links.json")
downloaded_vod_links = json.load(jsonFile2)
gc.enable()


def analyze_all_vods():
    global user_index
    usernames = []
    links = []
    start_times = []
    vod_ids = []
    total_lines = 0
    with open('D:/ResetEfficiency/vodInfo.txt', "r+") as vodInfo:
        mm = mmap.mmap(vodInfo.fileno(), 0)
        while mm.readline():
            total_lines += 1
        for i1 in range(total_lines):
            line = vodInfo.readline()
            line = line.replace('\n', '')
            if i1 % 5 == 0:
                usernames.append(line)
            if i1 % 5 == 1:
                links.append(line)
            if i1 % 5 == 2:
                start_times.append(line)
            if i1 % 5 == 3:
                vod_ids.append(int(line[0:4]))
    if len(os.listdir(path1 + 'vods')) == len(vod_ids):
        for i2 in range(len(vod_ids)):
            vodpath = Path(path1 + "vods/" + str(vod_ids[i2]).zfill(4) + usernames[i2] + '.mp4')
            parts = list(vodpath.parts)
            vod = parts[len(parts) - 1]
            for i3 in range(len(runners)):
                if runners[i3]['twitch_name'] in vod:
                    user_index = i3
            if runners[user_index]['twitch_name'] not in ['makattak11', 'semperzz', 'specnr']:
                dict1 = {'user_index': user_index, 'sheetnames': runners[user_index]['sheet_names'], 'vodpath': str(vodpath), 'start_time': start_times[i2]}
                with open(path1 + 'arguments.json', 'w') as jsonFile:
                    json.dump(dict1, jsonFile)
                results = subprocess.run('py analyzeVod_sub.py')
                print(results)
    else:
        print("error2")


analyze_all_vods()
