# -*- coding: utf-8 -*-

import os.path
import subprocess
import shutil

def split(filename):
    basename = os.path.basename(filename)
    basepath = "C:\\Users\\314\\Documents\\book\\target2\\" + basename[:-4]
    print(basename)
    #subprocess.Popen(['convert', '-quality', '90', '-crop', crop_option, filename, basename + '_2.jpg'], stdout=subprocess.PIPE, shell=True)
    command = 'magick "' + "C:\\Users\\314\\Documents\\book\\" + filename + '" -crop 2x1@ +repage "' + basepath + '_%01d.jpg"'
    print(command)
    subprocess.call(command, shell=True)
    
    shutil.move(basepath + '_0.jpg', basepath + '_2.jpg')
    
def all():
    path = "target"
    dirs = os.listdir(path)
    for item in dirs:
        split(path + "\\" + item)
all()