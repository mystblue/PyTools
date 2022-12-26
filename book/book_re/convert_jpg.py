# -*- coding: utf-8 -*-

import configparser
import os
import os.path
import subprocess
import time

class CommandExecutor():
    def __init__(self):
        self.COMMAND = 'magick "{0}" -quality 90 "{1}"'

    def execute(self, src, dst):
        command = self.COMMAND.format(src, dst)
        #print(command)
        subprocess.call(command, shell=True)

def crop_png(src_path, dst_path):
    executor = CommandExecutor()
    executor.execute(src_path, dst_path)

def convert():
    config_ini = configparser.ConfigParser()
    config_ini_path = 'config.ini'
    config_ini.read(config_ini_path, encoding='utf-8')
    src = config_ini.get('DEFAULT', 'src')
    dst = config_ini.get('DEFAULT', 'cutted')

    folders = os.listdir(src)
    for folder_name in folders:
        folder_path = os.path.join(src, folder_name)
        if not os.path.isdir(folder_path):
            continue
        print(folder_name)
        dst_folder_path = os.path.join(dst, folder_name)
        if not os.path.exists(dst_folder_path):
            os.mkdir(dst_folder_path)

        folders = os.listdir(folder_path)
        for file in folders:
            file_path = os.path.join(folder_path, file)
            basename, ext = os.path.splitext(file)
            dst_file_path = os.path.join(dst_folder_path, basename + ".jpg")
            crop_png(file_path, dst_file_path)

            time.sleep(0.01)

if __name__ == '__main__':
    convert()