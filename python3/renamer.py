# -*- coding: utf-8 -*-

__author__ = "mystblue"
__version__ = "0.1.0"
__email__ = "mysterious.blue.star@gmail.com"

import os
import shutil
import subprocess

def main():
    out = "26"
    if not os.path.exists(out):
        os.makedirs(out)
    dirs = os.listdir("Nikuhisyo Yukiko v26")
    counter = 1
    for file in dirs:
        print(file)
        command = "magick \""
        command += os.path.join("Nikuhisyo Yukiko v26", file)
        command += "\" -crop 690x989+615+46 \""
        command += os.path.join(out, "{:04d}".format(counter) + ".png")
        command += "\""
        print(command)
        subprocess.call(command, shell=True)
        counter += 1

if __name__ == '__main__':
    main()