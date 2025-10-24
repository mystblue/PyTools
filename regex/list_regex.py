import json
import os

def process_file(file_name):
    ret = ""
    fullpath = os.path.join("schema", file_name)
    with open(fullpath, "r", encoding="utf-8") as fp:
        json_obj = json.load(fp)
        #print(json_obj)
        for category in json_obj:
            for item in category["request"]:
                ret += "/" + item["validRule"] + "/\n"
    return ret

def main():
    buf = ''
    folders = os.listdir("schema")
    for file_name in folders:
        #print(file_name)
        buf += process_file(file_name)
    
    print(buf)
    with open("regex_list.txt", "w", encoding="utf-8") as fw:
        fw.write(buf)

if __name__ == '__main__':
    main()
