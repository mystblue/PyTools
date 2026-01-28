
import os
import glob
from PIL import Image
import subprocess
import yaml

src = "src"
dst = "dst"

def read_yaml():
	with open('key.yml', 'r', encoding="utf-8") as yml:
	    ap = yaml.safe_load(yml)
	    
	    dic = ap['key']
	    return dic

def create_index(dst_path, title, folder_list):
    buf = ""
    with open("template\\index.html", "r", encoding="utf-8") as f:
        buf = f.read()
    
    dic = read_yaml()
    print(folder_list)
    table = ""
    row = "<tr><td>{0}</td><td>{1}</td><td></td><td></td></tr>\n"
    for folder in folder_list:
        name = basename = os.path.basename(folder)
        splitted = name.split("_")
        #print(splitted)
        table += row.format(title, splitted[1])
    
    buf = buf.format(title, dic[title], table)
    dst_file_path = os.path.join(dst_path, "index.html")
    with open(dst_file_path, "w", encoding="utf-8") as f:
        f.write(buf)

def create_jpg_one(folder, dst_path, episode):
    main_list = []
    current_list = []
    main_list.append(current_list)
    height = 0
    
    folders = os.listdir(folder)
    for file_name in folders:
        #print(file_name)
        filepath = os.path.join(folder,file_name)
        img = Image.open(filepath)
        w, h = img.size
        height += h
        if height > 65500:
            #print("max")
            current_list = []
            main_list.append(current_list)
            height = h
        current_list.append(filepath)
        #print(h)
    
    count = 1
    for my_list in main_list:
        param = ""
        for file in my_list:
            param += file + " "
        command = "magick " + param + "-append " + dst_path + "\\" + episode + "_" + str(count) + ".jpg"
        #print(command)
        subprocess.call(command, shell=True)
        count += 1
    
def create_jpg(folder_list, dst_path):
    for folder in folder_list:
        name = basename = os.path.basename(folder)
        splitted = name.split("_")
        #print(folder)
        #print(splitted[1])
        create_jpg_one(folder, dst_path, splitted[1])

def create_html_one(title, folder, dst_path, episode):
    buf = ""
    with open("template\\template.html", "r", encoding="utf-8") as f:
        buf = f.read()
    
    dic = read_yaml()
    table = ""
    row = "<div class=\"flexbox\"><img id=\"myImage\" src=\"./{0}\" /></div>\n"

    dir_path = dst_path + "\\{e}*.jpg".format(e=episode)
    print(dir_path)
    files = glob.glob(dir_path)
    for file_path in files:
        file_name = os.path.basename(file_path)
        table += row.format(file_name)
    
    next = str(int(episode) + 1).zfill(3)
    
    buf = buf.format(title, dic[title], episode, next, table)
    dst_file_path = os.path.join(dst_path, episode + ".html")
    with open(dst_file_path, "w", encoding="utf-8") as f:
        f.write(buf)
    
def create_html(title, folder_list, dst_path):
    for folder in folder_list:
        name = basename = os.path.basename(folder)
        splitted = name.split("_")
        create_html_one(title, folder, dst_path, splitted[1])

def process_title(src, dst, title):
    title_path = os.path.join(src, title)
    folders = os.listdir(title_path)
    folder_list = []
    for folder in folders:
        #print(folder)
        folder_list.append(os.path.join(title_path, folder))
    #print(folder_list)

    # ディレクトリが存在しない場合、ディレクトリを作成する
    dst_path = os.path.join(dst, title)
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)
    create_index(dst_path, title, folder_list)
    #create_jpg(folder_list, dst_path)
    create_html(title, folder_list, dst_path)

def main(src, dst):
    folders = os.listdir(src)
    for title in folders:
        process_title(src, dst, title)

if __name__ == '__main__':
    main(src, dst)