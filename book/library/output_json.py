# -*- coding: utf-8 -*-

import csv
import ujson

BASE_PATH = '/storage/0123-4567/comic'

def read_csv(file):
    list = []
    with open(file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        data = [row for row in reader]
        # 先頭はヘッダとして削除
        data.pop(0)
        item = {}
        for row in data:
            if not ('series' in item and item['series'] == row[2]):
                item = {}
                item['series'] = row[2]
                item['list'] = []
                list.append(item)
            title = {}
            title['title'] = row[0]
            title['path'] = BASE_PATH + "/" + row[2] + "/" + row[1]
            item['list'].append(title)
    return list

def convert(inputname, outputname):
    list = read_csv(inputname)
    with open(outputname, 'w', encoding="utf-8") as f:
        p = ujson.dumps(list, indent=4, ensure_ascii=False)
        #p = ujson.dumps(list, indent=4, ensure_ascii=False)
        f.write(p)

if __name__ == '__main__':
    convert('comic.csv', 'book_recommend.json')