# -*- coding: utf-8 -*-

import os
import os.path
import subprocess
import time

class CommandExecutor():
    def __init__(self):
        self.COMMAND = 'magick "{0}" -resize 25% -quality 90 "{1}"'

    def execute(self, src, dst):
        command = self.COMMAND.format(src, dst)
        print(command)
        subprocess.call(command, shell=True)

def convert(src_path, dst_path):
    executor = CommandExecutor()
    executor.execute(src_path, dst_path)

def convert_folder():
    src = "test"
    dst = "test2"
    folders = os.listdir(src)
    for file in folders:
        file_path = os.path.join(src, file)
        dst_path = os.path.join(dst, file)
        convert(file_path, dst_path)

if __name__ == '__main__':
    convert_folder()
