# -*- coding: utf-8 -*-

# 分冊版をマージする
# splitted\
#   ↓
# cutted\

import configparser
import os
import os.path
import shutil

def merge():
    config_ini = configparser.ConfigParser()
    config_ini_path = 'config.ini'
    config_ini.read(config_ini_path, encoding='utf-8')
    src = config_ini.get('DEFAULT', 'splitted')
    dst = config_ini.get('DEFAULT', 'cutted')

    dst = os.path.join(dst, "a")
    if not os.path.exists(dst):
        os.mkdir(dst)

    folders = os.listdir(src)
    for split_folder_name in folders:
        split_folder_path = os.path.join(src, split_folder_name)
        folders = os.listdir(split_folder_path)
        for folder_name in folders:
            src_path = os.path.join(split_folder_path, folder_name)
            dst_path = os.path.join(dst, split_folder_name + "_" + folder_name)
            shutil.copyfile(src_path, dst_path)
    print("finish.")

if __name__ == '__main__':
    merge()
