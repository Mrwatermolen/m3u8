#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import json
import re
import locale
import sys
import time
import shutil
defaut_dir = "/home/pi/share/mh/torrent/AutoPush/"
home_dir = "/home/pi/"
image_config = "-U0 -n 12 -c 4 -H 200 -a 300/200"
#release_name = input("0day name")


def get_media_info(file):
    pname = 'mediainfo "%s" --Output=JSON' % (file)
    print(pname)
    result = subprocess.Popen(
        pname, shell=False, stdout=subprocess.PIPE).stdout
    list_std = result.readlines()
    str_tmp = ''
    for item in list_std:
        str_tmp += bytes.decode(item.strip())
    print(str_tmp)
    #json_data = json.loads(str_tmp)
    #print(json_data)
    return str_tmp


def creat_image_contract_sheet(video_file, save_path):
    command = "bash " + home_dir + "vcs.bash " + \
        video_file + " " + image_config + " -o " + save_path
    subprocess.Popen(command, shell=False)


if (__name__ == '__main__'):
    file = input("\n input video file path \n")
    #defaut_dir += release_name
    #print(defaut_dir)

    media_info = get_media_info(file)
    #with open(defaut_dir + "info.txt", "w") as f:
        #f.write(media_info)
