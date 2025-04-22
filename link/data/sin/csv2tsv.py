
def main(in_filename, out_filename):
    print("■" + in_filename)
    buf = ''
    with open(in_filename, "r", encoding="utf-8") as f:
        buf = f.read()
    
    lines = buf.split('\n')
    
    ret = ""
    
    for line in lines:
        if line == '':
            continue
        
        first_index = line.index("\"{")
        last_index = line.index("}\"")
        
        before = line[1:first_index-2]
        last = line[last_index+4:-1]
        
        before = before.replace('","', "\t")

        first_index2 = last.index("\"{")
        last_index2 = last.index("}\"")

        before2 = last[0:first_index2-2]
        last2 = last[last_index2+4:]

        before2 = before2.replace('","', "\t")
        last2= last2.replace('","', "\t")

        ret += before + "\t" + line[(first_index+1):(last_index+1)] + "\t" + before2 + "\t" +  last[(first_index2+1):(last_index2+1)] + "\t" + last2 + "\n"

    with open(out_filename, "w", encoding="utf-8") as f:
        f.write(ret)

if __name__ == '__main__':
    main("result20250416_1_dup.csv", "result20250416_1_dup.tsv")
    main("result20250416_2_dup.csv", "result20250416_2_dup.tsv")
