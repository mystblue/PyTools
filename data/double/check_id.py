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

def main(filename_d, filename):
    buf_d = ''
    with open(filename_d, "r", encoding="utf-8") as f:
        buf_d = f.read()
    lines_d = buf_d.split('\n')

    buf = ''
    with open(filename, "r", encoding="utf-8") as f:
        buf = f.read()
    lines = buf.split('\n')

    ret = ""
    for lined in lines_d:
        ret += lined
        if len(lined) == 0:
            continue
        for i in range(0, len(lines)):
            if lines[i] == lined:
                ret += " " + str(i+1) + "行目"
        ret += "\n"

    with open("result.txt", "w", encoding="utf-8") as f:
        f.write(ret)

if __name__ == '__main__':
    #main("id_d.txt", "id.txt")
    main("ttyid_d.txt", "ttyid.txt")
