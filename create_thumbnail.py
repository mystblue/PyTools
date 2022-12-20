# -*- coding: utf-8 -*-

# cbz から表紙のサムネイル画像を生成する
# -resize 200x200 オプションで画像を生成する

import configparser
import io
import os
import os.path
import subprocess
import sys
import zipfile

cover_file_name_png = "0001.png"
cover_file_name_jpg = "0001.jpg"

option = "200x200"

class CommandExecutor():
    def __init__(self):
        self.COMMAND = 'magick "{0}" -resize {1} "{2}"'

    def execute(self, src, dst, option):
        command = self.COMMAND.format(src, option, dst)
        print(command)
        subprocess.call(command, shell=True)

def create_image(src_path, dst_path, option):
    executor = CommandExecutor()
    executor.execute(src_path, dst_path, option)

def create_cover_file(zip_file):
    with zipfile.ZipFile(zip_file) as myzip:
        file_list = myzip.namelist()
        cover_file_name = ""
        if cover_file_name_jpg in file_list:
            cover_file_name = cover_file_name_jpg
        elif cover_file_name_png in file_list:
            cover_file_name = cover_file_name_png
        else:
            print("表紙の画像が見つかりません。")
            sys.exit(0)
        with myzip.open(cover_file_name) as img_file:
            img_bin = img_file.read()  # メモリ上のデータを読み込む
            with open(cover_file_name, "wb") as fw:
                fw.write(img_bin)
        return cover_file_name

def create_thumbnail():
    src = "."
    
    folders = os.listdir(src)
    for file_name in folders:
        file_path = os.path.join(src, file_name)
        cover_file_name = create_cover_file(file_path)
        dst = os.path.splitext(os.path.basename(file_name))[0] + ".jpg"
        create_image(cover_file_name, dst, option)
        os.remove(cover_file_name)

    print("finish.")

if __name__ == '__main__':
    create_thumbnail()
