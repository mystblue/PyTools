# -*- coding: utf-8 -*-

import os
import time


max = 171

folder_name = 'ヴァンプコミックス_佐原玄清_セックス＆ダンジョン！！_07_dmm_20220722'

if __name__ == '__main__':
    os.system('adb shell mkdir ' + '/sdcard/scshot/{}'.format(folder_name))
    for i in range(1, max + 1):
        output_path = '/sdcard/scshot/{}/{:04}.png'.format(folder_name, i)
        print(output_path)
        os.system('adb shell screencap -p ' + output_path)
        os.system('adb shell input touchscreen swipe 500 500 1500 500')
        #reverse
        #os.system('adb shell input touchscreen swipe 1000 500 500 500')
        time.sleep(0.5)
