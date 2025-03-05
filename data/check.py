
def main(filename):
    print("■" + filename)
    buf = ''
    with open(filename, "r", encoding="utf-8") as f:
        buf = f.read()
    
    lines = buf.split('\n')
    
    ret = ""
    
    for i in range(1, len(lines)-1):
        #print(lines[i])
        index = lines[i].find("jp.co.fngate.docan")
        if index != -1:
            checkStr = lines[i][index + len("jp.co.fngate.docan"): index + len("jp.co.fngate.docan") + 10]
            ret += "○" + checkStr + "\n"

    with open("result.txt", "w", encoding="utf-8") as f:
        f.write(ret)

if __name__ == '__main__':
    main("target.txt")
