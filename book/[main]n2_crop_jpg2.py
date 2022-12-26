# -*- coding: utf-8 -*-

import configparser
import os
import os.path
import subprocess
import time
from book_crop import get_book_crop_dict

class CommandExecutor():
    def __init__(self):
        self.COMMAND = 'magick "{0}" -crop {1} -quality 90 "{2}"'

    def execute(self, src, dst, option):
        command = self.COMMAND.format(src, option, dst)
        #print(command)
        subprocess.call(command, shell=True)

def crop_png(src_path, dst_path, option):
    executor = CommandExecutor()
    executor.execute(src_path, dst_path, option)

if __name__ == '__main__':
    config_ini = configparser.ConfigParser()
    config_ini_path = 'config.ini'
    config_ini.read(config_ini_path, encoding='utf-8')
    src = config_ini.get('DEFAULT', 'src')
    dst = config_ini.get('DEFAULT', 'dst')

    dict = get_book_crop_dict()

    folders = os.listdir(src)
    for folder_name in folders:
        option = ''
        try:
            option = dict[folder_name]
        except:
            print("設定が見つかりませんでした" + folder_name)
            continue

        folder_path = os.path.join(src, folder_name)
        if not os.path.isdir(folder_path):
            continue
        print(folder_name)
        # 出力先
        dst_folder_path = os.path.join(dst, folder_name)
        if not os.path.exists(dst_folder_path):
            os.mkdir(dst_folder_path)

        # 各ファイル
        folders = os.listdir(folder_path)
        for file in folders:
            file_path = os.path.join(folder_path, file)
            basename, ext = os.path.splitext(file)
            dst_file_path = os.path.join(dst_folder_path, basename + ".jpg")
            crop_png(file_path, dst_file_path, option)

            time.sleep(0.01)
