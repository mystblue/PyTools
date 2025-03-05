import os
import os.path

def check_log(filename, sn):
    print("■" + filename)
    buf = ''
    with open(filename, "r", encoding="utf-8") as f:
        buf = f.read()
    
    lines = buf.split('\n')
    
    ret = ""
    
    for i in range(0, len(lines)):
        #print(lines[i])
        index = lines[i].find(sn)
        if index != -1:
            ret += lines[i] + "\n"
    return ret

def main(foldername, sn):
    ret = ""
    folders = os.listdir(foldername)
    for file_name in folders:
        #print(file_name)
        ret += check_log(os.path.join(foldername, file_name), sn)
    with open("result.txt", "w", encoding="utf-8") as f:
        f.write(ret)

if __name__ == '__main__':
    main("logs", "P211211C00517")
