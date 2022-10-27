# -*- coding: utf-8 -*-

"""
"""

__author__  = 'mystblue'
__version__ = '1.0.0'

def main():
    ret_list = []
    with open("cert/certlist.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip('\r\n')
            splited = line.split("  ")
            ret_list.extend(splited)

    for item in ret_list:
        print(item)
    print(len(ret_list))
    with open("cert/file_list.txt", "w", encoding="utf-8") as fw:
        for item in ret_list:
            fw.write(item + "\n")

if __name__ == '__main__':
    main()
