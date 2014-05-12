# encoding: utf-8

"""
画像を切り出すスクリプト
"""

__author__  = 'kayama'
__version__ = '0.1'
__date__    = '2014/05/09'

from PIL import Image

def cut_img(img_path, offsetX, offsetY, prefix):
    im = Image.open(img_path + ".png")
    box = (0 + offsetX, 216 + offsetY, 216 + offsetX, 432 + offsetY)
    im2 = im.crop(box)
    im2.save(prefix + '1.png', 'png')

    box = (216 + offsetX, 0 + offsetY, 432 + offsetX, 216 + offsetY)
    im3 = im.crop(box)
    im3.save(prefix + '2.png', 'png')

    box = (216 + offsetX, 216 + offsetY, 432 + offsetX, 432 + offsetY)
    im4 = im.crop(box)
    im4.save(prefix + '.png', 'png')

    box = (432 + offsetX, 216 + offsetY, 648 + offsetX, 432 + offsetY)
    im5 = im.crop(box)
    im5.save(prefix + '3.png', 'png')

    box = (216 + offsetX, 432 + offsetY, 432 + offsetX, 648 + offsetY)
    im6 = im.crop(box)
    im6.save(prefix + '4.png', 'png')

    im7 = Image.open(img_path + "2.png")
    box = (216 + offsetX, 216 + offsetY, 432 + offsetX, 432 + offsetY)
    im8 = im7.crop(box)
    im8.save(prefix + '_e.png', 'png')

if __name__ == '__main__':
    cut_img("animal", 1, 0, "flick_aml")
    cut_img("food", 1, 0, "flick_fod")
    cut_img("cafe", 1, 0, "flick_caf")
    cut_img("ball", 1, 0, "flick_spt")
    cut_img("fruits", 1, 0, "flick_frt")
    cut_img("music", 1, 0, "flick_msc")
    cut_img("nature", 1, 0, "flick_ntr")
    cut_img("pc", 1, 0, "flick_cmp")
    cut_img("sea", 0, 0, "flick_sea")
    cut_img("space", 0, 0, "flick_spc")
    cut_img("vehicle", 1, 0, "flick_vcl")
    cut_img("weather", 0, 0, "flick_wth")
    