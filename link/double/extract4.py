
def main(filename):
    print("■" + filename)
    buf = ''
    with open(filename, "r", encoding="utf-8") as f:
        buf = f.read()
    
    lines = buf.split('\n')
    
    ret = ""
    
    for i in range(1, len(lines)-1):
        #print(lines[i])
        if not lines[i].endswith("1"):
            ret += lines[i] + "\n"

    with open("multi4.csv", "w", encoding="utf-8") as f:
        f.write(ret)

if __name__ == '__main__':
    main("result4.csv")
