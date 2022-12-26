# -*- coding: utf-8 -*-

import configparser
import os
import os.path
import shutil

def delete_folder(path):
    folders = os.listdir(path)
    for folder_name in folders:
        folder_path = os.path.join(path, folder_name)
        if not os.path.isdir(folder_path):
            continue
        print("x -> " + folder_name)
        shutil.rmtree(folder_path)

def clean():
    config_ini = configparser.ConfigParser()
    config_ini_path = 'config.ini'
    config_ini.read(config_ini_path, encoding='utf-8')
    src = config_ini.get('DEFAULT', 'src')
    cutted = config_ini.get('DEFAULT', 'cutted')

    folders = os.listdir(src)
    for option_name in folders:
        option = option_name
        print(option)
        option_folder_path = os.path.join(src, option_name)
        delete_folder(option_folder_path)
    print("cutted")
    delete_folder(src)
    delete_folder(cutted)
    print("finish.")

if __name__ == '__main__':
    clean()