import datetime

def get_data(item):
    if item == '':
        return None
    items = item.split(",")
    return items[0], items[1]

def check(item1, item2):
    data1 = get_data(item1)
    data2 = get_data(item2)
    format = '%Y-%m-%d %H:%M:%S'
    dt1 = datetime.datetime.strptime(data1[1], format)
    dt2 = datetime.datetime.strptime(data2[1], format)
    timedelta = dt2 - dt1
    if timedelta.seconds < 6:
        #print(timedelta.seconds)
        if data1[0]  == data2[0]:
            print(data1[0] + " : " + data1[1])
            print(data2[0] + " : " + data2[1])

def main(filename):
    print("■" + filename)
    buf = ''
    with open(filename, "r", encoding="utf-8") as f:
        buf = f.read()
    
    lines = buf.split('\n')
    
    count = len(lines)
    
    for i in range(1, count -2):
        check(lines[i], lines[i + 1])

if __name__ == '__main__':
    main("result3.csv")
