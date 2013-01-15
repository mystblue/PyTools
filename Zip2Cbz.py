# -*- coding: utf-8 -*-

"""
同階層にある zip ファイルの拡張子を cbz に変更するスクリプト。
"""

__author__  = 'mystblue'
__version__ = '0.0.1'

import os
import re
import Tkinter
import tkMessageBox
import zipfile

def message():
    """
    終了メッセージを表示する
    """
    root = Tkinter.Tk()
    root.withdraw()

    tkMessageBox.showinfo("finish", "finished.")


def getExtension(filename):
    """
    指定したパスの拡張子を取得する
    """
    root, ext = os.path.splitext(filename)
    return ext

def isZipfile(filename):
    """
    zip ファイルかどうか
    """
    if getExtension(filename) == '.zip':
        return True
    else:
        return False

def searchDir(rootDir):
    """
    rootDir 直下に zip ファイルがあれば、cbz に変更する
    """
    fileList = os.listdir(rootDir)
    for item in fileList:
        if os.path.isfile(os.path.join(rootDir, item)):
            if isZipfile(item):
                print item
                os.rename(os.path.join(rootDir, item), os.path.join(rootDir, item)[:-4] + '.cbz')

if __name__ == "__main__":
    searchDir(".")
    message()
