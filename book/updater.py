# -*- coding: utf-8 -*-

"""
本のファイル名をチェックするスクリプト
"""

__author__  = 'mystblue'
__version__ = '1.0.0'

import json
import os

#FOLDER_PATH = "test"
#FOLDER_PATH = "zip"
FOLDER_PATH = "E:\\master"

def main():
    folders = os.listdir(FOLDER_PATH)
    json_obj = []
    for file_name in folders:
        filename = basename_without_ext = os.path.splitext(os.path.basename(file_name))[0]
        splitted = filename.split("_")
        
        dic = {}

        # 前処理として、ファイル形式をチェック
        last = splitted[len(splitted) - 1]
        if last == "crop-png":
            dic["形式"] = "crop-png"
            del splitted[-1]
        elif last == "crop-jpg":
            dic["形式"] = "crop-jpg"
            del splitted[-1]
        elif last == "download":
            dic["形式"] = "download"
            del splitted[-1]
        elif last == "scan":
            dic["形式"] = "scan"
            del splitted[-1]
        else:
            dic["形式"] = "master-zip"

        if len(splitted) == 5:
            dic["レーベル"] = splitted[0]
            dic["著者"] = splitted[1]
            dic["タイトル"] = splitted[2]
            dic["巻数"] = ""
            dic["ストア"] = splitted[3]
            dic["入手日"] = splitted[4]
            dic["ファイル名"] = file_name
    
            new_file_name = dic["レーベル"] + "_" + dic["著者"] + "_" + dic["タイトル"] + "_" + dic["巻数"] + "_" + dic["ストア"] + "_" + dic["入手日"] + ".zip"
            print(file_name + " → " + new_file_name)
            path1 = os.path.join(FOLDER_PATH, file_name)
            path2 = os.path.join(FOLDER_PATH, new_file_name)
            os.rename(path1, path2)

if __name__ == '__main__':
    main()
