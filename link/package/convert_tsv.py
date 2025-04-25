import re

def main(src, dst):
    print("■" + src)
    buf = ''
    with open(src, "r", encoding="utf-8") as f:
        buf = f.read()
    
    lines = buf.split('\n')
    
    ret = ""
    
    for line in lines:
        if line == '':
            continue
        index = line.index(' - ')
        
        match = re.search('(\\-[0-9]+\\.)', line[:index])
        if match:
            #print(match.group(1))
            str = match.group(1)
            index2 = line.index(str)
        else:
            #print("error = " + line)
            match2 = re.search('(\\-[0-9]+)', line[:index])
            if match2:
                #print(match.group(1))
                str = match2.group(1)
                index2 = line.index(str)
            else:
                print("error2 = " + line[:index])
        
        ret += line[:index2] + "\t" + line[index2+1:index] + "\t" + line[index + 3:] + "\n"

    with open(dst, "w", encoding="utf-8") as f:
        f.write(ret)

if __name__ == '__main__':
    main("gw_nginx_installed.txt", "gw_nginx_installed.tsv")
    main("gw_php-fpm_installed.txt", "gw_php-fpm_installed.tsv")
    main("testtool_installed.txt", "testtool_installed.tsv")
    main("tms_nginx_installed.txt", "tms_nginx_installed.tsv")
    main("tms_php-fpm_installed.txt", "tms_php-fpm_installed.tsv")
    main("tmsweb_nginx_installed.txt", "tmsweb_nginx_installed.tsv")
    main("tmsweb_php-fpm_installed.txt", "tmsweb_php-fpm_installed.tsv")
    main("ca_installed.txt", "ca_installed.tsv")
