# coding: utf-8

"""
同階層にあるフォルダを zip 圧縮するスクリプト。
ただし、拡張子は、cbz とする。
フォルダ内のファイル名は 4 桁の連番となる。
フォルダ名が ( や - で始まる場合はスキップされる
"""

import configparser
import os
import re
import subprocess
import zipfile

def show_message(num):
    """
    メッセージを出力する
    """

    if num ==0:
        print("フォルダが見つかりませんでした。")
    else:
        print(str(num) + "個のフォルダを圧縮しました。")
    #subprocess.call('pause', shell=True)

def is_img(ext):
    """
    画像ファイルかどうか
    """
    img_list = [".jpg", ".png", ".gif", ".bmp", ".jpeg"]
    if ext.lower() in img_list:
        return True
    else:
        return False

def get_ext(filename):
    """
    指定したファイル名の拡張子を取得する
    """
    root, ext = os.path.splitext(filename)
    return ext

def zip_compress(path, dst_path):
    """
    ZIP 圧縮を行う
    """
    output_path = os.path.join(dst_path, os.path.basename(path))
    zip = zipfile.ZipFile(output_path + ".cbz", 'w', zipfile.ZIP_DEFLATED)
    file_list = os.listdir(path)
    #file_list = sort(file_list)
    counter = 1
    for file_name in file_list:
        if not is_img(get_ext(file_name)):
            continue
        zip.write(os.path.join(path, file_name),
                  file_name)
        counter = counter + 1
    zip.close()

def search_folder(rootDir, dst_path):
    """
    rootDir 直下にフォルダがあれば、zip 圧縮する
    """
    count = 0
    file_list = os.listdir(rootDir)
    for file_name in file_list:
        path = os.path.join(rootDir, file_name)
        # ファイルは処理しない
        if not os.path.isdir(path):
            continue
        # ( や - で始まるフォルダも処理しない
        if file_name.startswith('+') or file_name.startswith('-'):
            continue
        #print file_name
        zip_compress(path, dst_path)
        count = count + 1
    return count

def compress():
    config_ini = configparser.ConfigParser()
    config_ini_path = 'config.ini'
    config_ini.read(config_ini_path, encoding='utf-8')
    src = config_ini.get('DEFAULT', 'cutted')
    dst = config_ini.get('DEFAULT', 'cbz')
    num = search_folder(src, dst)
    show_message(num)

if __name__ == '__main__':
    compress()