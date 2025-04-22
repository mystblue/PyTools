import datetime

def str2datetime(str):
    format = '%Y-%m-%d %H:%M:%S'
    dt = datetime.datetime.strptime(str, format)
    return dt

def process(items):
    ret = ""
    dt_list = []
    for item in items:
        tabbed = item.split('\t')
        dt_list.append(str2datetime(tabbed[2]))
    
    flag = 0
    for i in range(len(dt_list) - 1):
        dt1 = dt_list[i]
        dt2 = dt_list[i+1]
        timedelta = dt2 - dt1
        print(timedelta.seconds)
        if timedelta.days == 0 and timedelta.seconds < 3600:
            flag = 1
        else:
            if flag == 0:
                flag == 2
    
    append = "\tWithin1hour\n"
    if flag == 2:
        append = "\tNone\n"
    
    for item in items:
        ret += item + append
    return ret

def main(in_filename, out_filename):
    print("■" + in_filename)
    buf = ''
    with open(in_filename, "r", encoding="utf-8") as f:
        buf = f.read()
    
    lines = buf.split('\n')
    
    ret = ""
    
    current = ""
    process_list = []
    
    try:
        while True:
            line = lines.pop(0)
            tabbed = line.split('\t')
            check_item = tabbed[-1]
            if current == "":
                current = check_item
                process_list.append(line)
            else:
                if current == check_item:
                    process_list.append(line)
                else:
                    ret = process(process_list)
                    process_list.clear()
                    current = check_item
                    process_list.append(line)
    except IndexError as e:
        #ret = process(process_list)
        pass

    with open(out_filename, "w", encoding="utf-8") as f:
        f.write(ret)

if __name__ == '__main__':
    main("result20250416_1_dup.tsv", "result20250416_1_dup_mark.tsv")
    #main("result20250416_2_dup.tsv", "result20250416_2_dup_mark.tsv")
