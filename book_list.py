# encoding: utf-8

"""
"""

import os

#file_path = "file_list.txt"
file_path = "master_list.txt"

def is_folder(str):
    str = os.path.basename(str)
    if "." in str:
        return False
    else:
        return True

def main():
    book_list = []
    with open(file_path, "r", encoding="cp932") as f:
        for line in f:
            line = line.rstrip('\r\n')
            if is_folder(line):
                continue
            line = os.path.basename(line)

            filename = os.path.splitext(line)[0]

            splitted = filename.split('_')
            #if len(splitted) != 5:
            #    print(filename)

            if len(splitted) == 5:
                if not splitted[2].isdigit():
                    print("巻数が間違っています。" + filename)
                    continue
                if not splitted[4].isdigit():
                    print("日付が間違っています。" + filename)
                    continue
                book_list.append(splitted)

    print(len(book_list))
    #book_list.sort(key = lambda x:x[4], reverse = False)
    book_list.sort(key = lambda x:x[1], reverse = False)

    with open("result_title.csv", "w", encoding="utf-8") as fw:
        for book in book_list:
            for item in book:
                fw.write(item)
                fw.write(",")
            fw.write("\n")

if __name__ == '__main__':
    main()