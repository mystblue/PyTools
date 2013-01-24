# -*- coding: utf-8 -*-

"""
同階層以下にあるフォルダおよびファイルを result.txt として出力する
"""

import os

class FileList:
    def __init__(self):
        self.buf = ""
        self.path = "."
        self.level = 0

    def outputDir(self, path, level):
        dirs = os.listdir(path)
        for dir in dirs:
            if os.path.isdir(os.path.join(path, dir)):
                self.buf = self.buf + "    " * level + "[" + dir + "]" + "\r\n"
                self.outputDir(os.path.join(path, dir), level + 1)
            else:
                self.buf = self.buf + "    " * level + "・" +  dir + "\r\n"

    def writeFile(self, filename):
        with open(filename, "wb") as f:
            f.write(self.buf)

if __name__ == "__main__":
    fl = FileList()
    fl.outputDir(".", 0)
    fl.writeFile("result.txt")
