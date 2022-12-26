# -*- coding: utf-8 -*-

import convert_jpg
import cbz_compress
import clean

if __name__ == '__main__':
    convert_jpg.convert()
    cbz_compress.compress()
    clean.clean()
