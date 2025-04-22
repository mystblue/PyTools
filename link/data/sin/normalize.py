import datetime

def str2datetime(str):
    format = '%Y-%m-%d %H:%M:%S'
    dt = datetime.datetime.strptime(str, format)
    return dt

def process(items):
    ret = ""
    dt_list = []
    for item in items:
        if item == "":
            continue
        tabbed = item.split('\t')
        dt_list.append(str2datetime(tabbed[2]))
    
    flag = 0
    for i in range(len(dt_list) - 1):
        dt1 = dt_list[i]
        dt2 = dt_list[i+1]
        timedelta = dt2 - dt1
        if timedelta.days == 0 and timedelta.seconds < 3600:
            flag = 1
        else:
            if flag == 0:
                flag = 2
    
    append = "\tWithin1hour\n"
    if flag == 2:
        append = "\tNone\n"
    
    # 報告済み 
    if tabbed[-1] == "20241007_SC252A_720" or tabbed[-1] == "20241117_C7228Q_1440" or tabbed[-1] == "20241220_BJ22G8_41400":
        append = "\tReported\n"

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
            check_item = tabbed[-1]
            amount = tabbed[-2]
            last_index = line.rfind('\t')
            
            request_date = tabbed[2]
            request_date = request_date.replace("-", "")
            request_date = request_date[0:8]
            
            check_param = request_date + "_" + check_item + "_" + amount
            ret += line[:last_index] + "\t" + check_param + "\n"
    except IndexError as e:
        pass

    with open(out_filename, "w", encoding="utf-8") as f:
        f.write(ret)

if __name__ == '__main__':
    main("result20250416_2_dup.tsv", "result20250416_2_dup_normalized.tsv")
