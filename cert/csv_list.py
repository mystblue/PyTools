# -*- coding: utf-8 -*-

"""
"""

__author__  = 'mystblue'
__version__ = '1.0.0'

def main():
    ret_list = []
    skip = True
    with open("cert/Certificate_data_221018_020936.csv", "r", encoding="ms932") as f:
        for line in f:
            if skip:
                skip = False
                continue
            line = line.rstrip('\r\n')
            splited = line.split(",")
            ret_list.append(splited[len(splited) - 1])

    for item in ret_list:
        print(item)
    print(len(ret_list))
    with open("cert/db_list.txt", "w", encoding="utf-8") as fw:
        for item in ret_list:
            fw.write(item + "\n")

if __name__ == '__main__':
    main()
