import glob  

PATH = "C:\\Users\\314\\Documents\\git\\PyTools\\novel\\kage\\*.txt"
OUTPUT = "C:\\Users\\314\\Documents\\git\\PyTools\\novel\\kage.txt"

txt_files = glob.glob(PATH) ##拡張子が「*txt」だけのファイルを返す

print(type(txt_files))

ret = ""
for file in txt_files:  
    print(file)
    with open(file, "r", encoding="utf-8") as f:
        ret += f.read()

with open(OUTPUT, "w", encoding="utf-8") as fw:
    fw.write(ret)

