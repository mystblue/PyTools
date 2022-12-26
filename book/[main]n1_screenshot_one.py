# -*- coding: utf-8 -*-

import os
import time

max = 28
folder_name = '真島ヒロ_FAIRY-TAIL_243'

if __name__ == '__main__':
    output_path = '/sdcard/scshot/0000.png'
    os.system('adb shell screencap -p ' + output_path)
