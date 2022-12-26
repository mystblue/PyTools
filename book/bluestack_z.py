import os
import time
from PIL import Image
from PIL import ImageGrab
import pyautogui

# zetman

max = 21
folder = "032"

kan = "桂正和_ZETMAN_03"
path = "C:\\Users\\myste\\Documents\\screenshot\\ZETMAN\\"
folder_path = os.path.join(path, kan)

def sc():
    for i in range(1, max + 1):
        filename = '{}_{:04}.jpg'.format(folder, i)
        file_path = os.path.join(folder_path, filename)
        #img = ImageGrab.grab(bbox=(135, 2, 1830, 1078))
        img = ImageGrab.grab()
        img = img.transpose(Image.ROTATE_270)
        img.save(file_path, 'JPEG', quality=90)

        pyautogui.moveTo(500,900)
        #pyautogui.click()
        pyautogui.mouseDown()
        pyautogui.moveTo(500,100, duration=0.5)
        pyautogui.mouseUp()
        time.sleep(1.2)

def dir():
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

if __name__ == '__main__':
    time.sleep(2)
    dir()
    sc()


# pip install Pillow
# pip install pyautogui


# full screen
#ImageGrab.grab().save("PIL_capture.png")

#ImageGrab.grab(bbox=(135, 0, 1795, 1080)).save(filename)

#filename_j = '{:04}.jpg'.format(i)
#img = Image.open(filename)
#img = img.transpose(Image.ROTATE_270)
#img.save(filename_j)

#os.system('adb shell input touchscreen swipe 500 500 1500 500')
