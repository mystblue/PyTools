# -*- coding: utf-8 -*-

"""
���K�w�ɂ��� zip �t�@�C���̊g���q�� cbz �ɕύX����X�N���v�g�B
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
    �I�����b�Z�[�W��\������
    """
    root = Tkinter.Tk()
    root.withdraw()

    tkMessageBox.showinfo("finish", "finished.")


def getExtension(filename):
    """
    �w�肵���p�X�̊g���q���擾����
    """
    root, ext = os.path.splitext(filename)
    return ext

def isZipfile(filename):
    """
    zip �t�@�C�����ǂ���
    """
    if getExtension(filename) == '.zip':
        return True
    else:
        return False

def searchDir(rootDir):
    """
    rootDir ������ zip �t�@�C��������΁Acbz �ɕύX����
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
