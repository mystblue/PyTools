# -*- coding: utf-8 -*-

import os
import time


max = 215

folder_name = 'splatoon2'

if __name__ == '__main__':
    # 出力先フォルダを作成
    os.system('adb shell mkdir ' + '/sdcard/scshot/{}'.format(folder_name))
    for i in range(1, max + 1):
        output_path = '/sdcard/scshot/{}/{:04}.png'.format(folder_name, max - i + 1)
        # ファミ通
        #output_path = '/sdcard/scshot/{}/{:04}.png'.format(folder_name, i)
        print(output_path)
        os.system('adb shell screencap -p ' + output_path)
        # 左閉じ ムックなど 左→右めくり
        os.system('adb shell input touchscreen swipe 500 500 1500 500')
        #reverse
        # 右閉じ 普通のコミック 右→左めくり
        #os.system('adb shell input touchscreen swipe 1000 500 500 500')
        time.sleep(0.5)
