import datetime

def str2datetime(str):
    format = '%Y-%m-%d %H:%M:%S'
    dt = datetime.datetime.strptime(str, format)
    return dt

def process(items):
    ret = ""
    
    append = "\t"
    
    # ３件以上
    if len(items) > 2:
        append = "\tF\n"
        for item in items:
            ret += item + append
        return ret
    
    tabbed1 = items[0].split('\t')
    tabbed2 = items[1].split('\t')
    # 報告済み 
    if tabbed1[0] == "14757589" or tabbed1[0] == "14757590" or tabbed1[0] == "15130393" or tabbed1[0] == "15130395" or tabbed1[0] == "15500725" or tabbed1[0] == "15500727" or tabbed1[0] == "16014350" or tabbed1[0] == "16014361":
        append = "\tE\n"
        for item in items:
            ret += item + append
        return ret

    # シリアル番号チェック
    if not tabbed1[6] == tabbed2[6]:
        append = "\tD\n"
        for item in items:
            ret += item + append
        return ret

    dt1 = str2datetime(tabbed1[2])
    dt2 = str2datetime(tabbed2[2])
    timedelta = dt2 - dt1
    
    if timedelta.days == 0 and timedelta.seconds < 300:
        append = "\tA\n"
    elif timedelta.days == 0 and timedelta.seconds < 3600:
        append = "\tB\n"
    else:
        append = "\tC\n"
    
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
            if line == "":
                continue
            tabbed = line.split('\t')
            check_item = tabbed[-3] #orderId
            if current == "":
                current = check_item
                current_list = []
                current_list.append(line)
                process_list.append(current_list)
            else:
                if current == check_item:
                    current_list.append(line)
                else:
                    current = check_item
                    current_list = []
                    current_list.append(line)
                    process_list.append(current_list)
    except IndexError as e:
        #ret = process(process_list)
        pass

    print(len(process_list))
    
    for item_list in process_list:
        ret += process(item_list)

    with open(out_filename, "w", encoding="utf-8") as f:
        f.write(ret)

if __name__ == '__main__':
    main("result20250416_1_dup.tsv", "result20250416_1_dup_mark.tsv")
    #main("result20250416_2_dup.tsv", "result20250416_2_dup_mark.tsv")
