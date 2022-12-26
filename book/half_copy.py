import os
import time
from PIL import Image
from PIL import ImageGrab
import win32clipboard
import win32gui
import io

# オリジナル

folder_path = "C:\\Users\\314\\Desktop\\sc\\"

def sc():
    filename = 'sc.png'
    file_path = os.path.join(folder_path, filename)
    #img = ImageGrab.grab(bbox=(135, 2, 1830, 1078))
    handle = win32gui.GetForegroundWindow() # 最前面のウィンドウハンドルを取得
    rect = win32gui.GetWindowRect(handle)   # ウィンドウの位置を取得
    img = ImageGrab.grab()
    img = img.crop(rect)
    #img = img.transpose(Image.ROTATE_270)
    img.save(file_path, 'PNG')

    output = io.BytesIO()
    img.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

if __name__ == '__main__':
    time.sleep(2)
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
