import os
import subprocess
import re
from pathlib import Path
import json


path1 = "D:/ResetEfficiency/"
max_videos_per_user = 10
jsonFile1 = open(path1 + "runners.json")
runners = json.load(jsonFile1)
jsonFile2 = open(path1 + "downloaded_vod_links.json")
downloaded_vod_links = json.load(jsonFile2)


def download_vod(url, name):
    subprocess.run(f'twitch-dl download {url} -f mp4 -q source -o {path1}vods/{name}.mp4')


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
    username_list = []
    for runner in runners:
        username_list.append(runner['twitch_name'])
    usernames, links, start_times = get_streams_info(username_list)
    existing_vod_paths = sorted(os.listdir(path1 + "vods"))
    last_vod = Path(existing_vod_paths[len(existing_vod_paths) - 1])
    last_vod_name = last_vod.parts[len(last_vod.parts) - 1]
    start_count = int(last_vod_name[0:4]) + 1

    for i in range(len(links)):
        if not (links[i] in downloaded_vod_links):
            download_vod(links[i], str(i + start_count).zfill(4) + usernames[i])
            downloaded_vod_links.append(links[i])
            vodInfo = (usernames[i], links[i], start_times[i], str(i + start_count).zfill(4))
            with open('D:/ResetEfficiency/vodInfo.txt', 'a') as f:
                for item in list(vodInfo):
                    f.writelines(item + '\n')
                f.writelines('\n')
            for dir in Path('C:/Users/thoma/AppData/Local/Temp/twitch-dl').glob('*'):
                for file in Path((str(dir) + '/chunked')).glob('*'):
                    os.remove(file)