import datetime


def main(in_filename, out_filename):
    print("■" + in_filename)
    buf = ''
    with open(in_filename, "r", encoding="utf-8") as f:
        buf = f.read()
    
    lines = buf.split('\n')
    
    ret = ""
    
    check_list = set()
    
    try:
        while True:
            line = lines.pop(0)
            if line == "":
                continue
            tabbed = line.split('\t')
            check_item = tabbed[0]
            check_list.add(check_item)
    except IndexError as e:
        pass

    for item_list in check_list:
        ret += item_list + "\n"

    with open(out_filename, "w", encoding="utf-8") as f:
        f.write(ret)

if __name__ == '__main__':
    main("result20250416_1_dup.tsv", "check_param_list.txt")
