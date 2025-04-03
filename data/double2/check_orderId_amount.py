import os
import os.path

def get_order_id(line):
    items = line.split('\t')
    return items[len(items) - 2]

def get_amount(line):
    items = line.split('\t')
    return items[len(items) - 1]

def check_dup(lines, order_id):
    ret = []
    for line in lines:
        if len(line) == 0:
            continue
        if get_order_id(line) == order_id:
            ret.append(line)
    
    amout_list = []
    for item in ret:
        amout_list.append(get_amount(item))
    
    org_list = set(amout_list)
    
    amout_list2 = []
    for org in org_list:
        if amout_list.count(org) > 1:
            amout_list2.append(org)
    
    ret2 = []
    for item in ret:
        amount = get_amount(item)
        if amount in amout_list2:
            ret2.append(item)
    
    return ret2

def get_dup_list():
    buf = ''
    with open("dup_orderid_list.csv", "r", encoding="utf-8") as f:
        buf = f.read()
    lines = buf.split('\n')
    return lines

def main(in_filename, out_filename):
    buf = ''
    with open(in_filename, "r", encoding="utf-8") as f:
        buf = f.read()
    lines = buf.split('\n')

    ret = ''
    for order_id in get_dup_list():
        if len(order_id) == 0:
            continue
        #print("[" + order_id + "]")
        list = check_dup(lines, order_id)
        for line in list:
            ret += line + '\n'

    with open(out_filename, "w", encoding="utf-8") as f:
        f.write(ret)

if __name__ == '__main__':
    main("result20250402.csv", "result.csv")
    #main("test.csv", "result.csv")
