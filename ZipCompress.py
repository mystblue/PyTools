# -*- coding: utf-8 -*-

"""
同階層にあるフォルダを zip 圧縮するスクリプト。
ただし、拡張子は、cbz とする。
"""

__author__  = 'mystblue'
__version__ = '0.0.1'

import os
import re
import Tkinter
import tkMessageBox
import zipfile

def message():
    root = Tkinter.Tk()
    root.withdraw()

    tkMessageBox.showinfo("finish", "finished.")

def compare(str1, str2):
    """
    a, a1 -> -1
    a11, a1 -> 1
    """
    l1 = len(str1)
    l2 = len(str2)
    min = l2 if l1 >= l2 else l1
    isSymbol = lambda x: True if re.match(r"\.|\?|-|_|\[|\]|\(|\)|\+|\*|/|<|>|\!|\"|#|\$|%|\&|'|=|~|\^|@|\{|\}|:|;", x) else False
    for i in range(min):
        s1 = str1[i]
        s2 = str2[i]
        if s1 == s2:
            continue
        else:
            if s1.isdigit() and s2.isdigit():
                i1 = i + 1
                i2 = i + 1
                while i1 < l1:
                    if str1[i1].isdigit():
                        s1 += str1[i1]
                    else:
                        break
                    i1 += 1
                while i2 < l2:
                    if str2[i2].isdigit():
                        s2 += str2[i2]
                    else:
                        break
                    i2 += 1
                # 001 と 01 の場合は、01 の方が大きい
                if long(s1) == long(s2):
                    return cmp(str1, str2)
                else:
                    return -1 if long(s1) < long(s2) else 1
            if isSymbol(s1) and not isSymbol(s2):
                return -1
            if not isSymbol(s1) and isSymbol(s2):
                return 1
    return cmp(str1, str2)

def getExt(filename):
    """
    指定したパスの拡張子を取得する
    """
    root, ext = os.path.splitext(filename)
    return ext

def getFilename(name, num):
    return '%04d' % num + getExt(name)

def zipCompress(path, dirName):
    """
    ZIP 圧縮を行う
    """
    parentDir = os.path.join(path, dirName)
    zip = zipfile.ZipFile(parentDir + ".cbz", 'w', zipfile.ZIP_DEFLATED)
    fileList = os.listdir(parentDir)
    counter = 1
    for item in fileList:
        zip.write(os.path.join(parentDir, item), getFilename(item, counter))
        counter = counter + 1
    zip.close()

def searchDir(rootDir):
    """
    rootDir 直下にフォルダがあれば、zip 圧縮する
    """
    fileList = os.listdir(rootDir)
    for item in fileList:
        if os.path.isdir(os.path.join(rootDir, item)):
            print item
            zipCompress(rootDir, item)

if __name__ == "__main__":
    searchDir(".")
    message()
