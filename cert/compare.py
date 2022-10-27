# -*- coding: utf-8 -*-

"""
"""

__author__  = 'mystblue'
__version__ = '1.0.0'

def file_to_list(file_name):
    ret_list = []
    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip('\r\n')
            ret_list.append(line)
    return ret_list

def main():
    file_list = file_to_list("cert/file_list.txt")
    db_list = file_to_list("cert/db_list.txt")

    no_list = []
    for db_item in db_list:
        if not db_item in file_list:
            no_list.append(db_item)

    for item in no_list:
        print(item)
    print(len(no_list))

if __name__ == '__main__':
    main()
