# -*- coding: utf-8 -*-

import crop_jpg
import merge
import cbz_compress
import clean

if __name__ == '__main__':
    crop_jpg.crop_jpg()
    merge.merge()
    cbz_compress.compress()
    clean.clean()
