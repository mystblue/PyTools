# -*- coding: utf-8 -*-

import configparser
import os
import os.path
import shutil

import crop_jpg
import crop_png
import crop_png2
import cbz_compress
import clean

if __name__ == '__main__':
    #crop_jpg.crop_jpg()
    #crop_png.crop_png()
    crop_png2.crop_png()
    cbz_compress.compress()
    clean.clean()