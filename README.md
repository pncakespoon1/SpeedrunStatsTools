# SpeedrunStatsTools
Tools which I'm working on to track stats of runs beyond what the typical tracker does

# Links
[Rawalle](https://github.com/joe-ldp/Rawalle)

[Grind-Simulator](https://github.com/Sharpieman20/grind-simulator)

[Specnr's Reset Tracker](https://github.com/Specnr/ResetTracker)

[Talking Mime's Reset Tracker](https://github.com/TheTalkingMime/ResetTracker)

[Efficiency Score Calculator](https://docs.google.com/spreadsheets/d/1lN_5Jbr5WdphUS2IR3Cc_LH2BSCXf7hJK5MGt6XsU-M/edit#gid=0)

[Stats Analysis Website](https://reset-analytics.vercel.app)


# Dependencies
pillow, tensorflow, numpy, cv2, pygsheets, twitch-dl, seaborn, scipy, pandas, matplotlib, keras-tuner, keras, pathlib

# Requirements
ffmpeg.exe and credentials.json in the folder, cuda

# Scripts

## analyzeVod.py
This is the heart of the program, it downloads a bunch of vods and writes various stats to a google sheet. It requires models in the models folder to detect buried treasures.

## makeImages.py
This script downloads a frame from every second of a vod specified to the unsorted_images folder. It requires a vod in the vods folder.

## breakWalls.py
This script "uncollages" wall images

## trainModel_bgss.py 
This script trains a model for classifying specific traits of spawn images. It requires images to be sorted in the designated folders in the spawn_image_classification folder. It stores the models in the models folder.

## trainModel_bt.py
This script trains a model for identifying buried treasure chest loot guis. It requires images to be sorted in the designated folders in the bt_identification folder. It stores the model in the models folder.

## trainModel_wall.py
This script trains a model for identifying wall interfaces. It requires images to be sorted in the designated folders in the wall_identification folder. It stores the model in the models folder.

# Credits
- Emily
- Ravalle
- Specnr
- Pokemon
- TalkingMime
- Lemon
