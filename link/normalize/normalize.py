
def convert_line(line):
    items = line.split("|")
    ret = []
    for item in items:
        if item == "":
            continue
        ret.append(item.strip())
    return ret

def main(filename):
    print("■" + filename)
    buf = ''
    with open(filename, "r", encoding="utf-8") as f:
        buf = f.read()
    
    lines = buf.split('\n')
    
    ret = ""
    
    for line in lines:
        if not line.startswith("|"):
            continue
        ret_list = convert_line(line)
        for item in ret_list:
            ret += item + "\t"
        ret = ret[:-1]
        ret += "\n"
    print(ret)
    with open("result.csv", "w", encoding="utf-8") as f:
        f.write(ret)

if __name__ == '__main__':
    main("20250404_二重決済履歴の確認.txt")
    #main("test.txt")
