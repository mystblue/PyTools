# -*- coding: utf-8 -*-

# cbz から表紙のサムネイル画像を生成する
# -resize 200x200 オプションで画像を生成する

import configparser
import io
import os
import os.path
import subprocess
import sys

class CommandExecutor():
    def __init__(self):
        self.COMMAND = 'magick "{0}" -alpha off "{1}"'

    def execute(self, src, dst):
        command = self.COMMAND.format(src, dst)
        print(command)
        subprocess.call(command, shell=True)

def create_image(src_path, dst_path):
    executor = CommandExecutor()
    executor.execute(src_path, dst_path)

def extract_alpha():
    src = 'yamato'
    
    folders = os.listdir(src)
    for file_name in folders:
        file_path = os.path.join(src, file_name)
        dst = os.path.splitext(os.path.basename(file_name))[0] + ".png"
        create_image(file_path, dst)

    print("finish.")

if __name__ == '__main__':
    extract_alpha()
