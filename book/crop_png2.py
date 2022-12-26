# -*- coding: utf-8 -*-

import configparser
import logger
import os
import os.path
import subprocess
import time

class CommandExecutor():
    def __init__(self):
        self.COMMAND = 'magick "{0}" -crop {1} "{2}"'

    def execute(self, src, dst, option):
        command = self.COMMAND.format(src, option, dst)
        print(command)
        subprocess.call(command, shell=True)

def crop_png2(src_path, dst_path, option):
    executor = CommandExecutor()
    executor.execute(src_path, dst_path, option)

def crop_png():
    # 処理前の時刻
    t1 = time.time() 
    log = logger.Logger("")
    
    config_ini = configparser.ConfigParser()
    config_ini_path = 'config.ini'
    config_ini.read(config_ini_path, encoding='utf-8')
    src = config_ini.get('DEFAULT', 'src')
    dst = config_ini.get('DEFAULT', 'dst')

    folders = os.listdir(src)
    for option_name in folders:
        option = option_name
        option_folder_path = os.path.join(src, option_name)
        folders = os.listdir(option_folder_path)
        print(option)
        for folder_name in folders:
            folder_path = os.path.join(option_folder_path, folder_name)
            if not os.path.isdir(folder_path):
                continue
            print(folder_name)
            log.log("[" + option + "] " + folder_name)
            dst_folder_path = os.path.join(dst, folder_name)
            if not os.path.exists(dst_folder_path):
                os.mkdir(dst_folder_path)

            folders = os.listdir(folder_path)
            for file in folders:
                file_path = os.path.join(folder_path, file)
                basename, ext = os.path.splitext(file)
                dst_file_path = os.path.join(dst_folder_path, basename + ".png")
                crop_png2(file_path, dst_file_path, option)

                time.sleep(0.01)
    # 処理後の時刻
    t2 = time.time()
    #print("finish.")
    # 経過時間を表示
    elapsed_time = t2-t1
    print(f"経過時間：{elapsed_time}")
    #subprocess.call('pause', shell=True)
