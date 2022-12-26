# -*- coding: utf-8 -*-

import os
import time


max = 190

folder_name = 'sh_06'
#folder_name = '008_04'
#folder_name = '494'
#folder_name = 'a157'
#folder_name = 'k032'
#folder_name = 'd033'
#folder_name = 'dai_184'

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
