import json

def check_file(lines, iv, sn, sver):
    ret = ""
    for i in range(0, len(lines)):
        index = lines[i].find(sn)
        if index != -1:
            index = lines[i].find(iv)
            if index != -1:
                index = lines[i].find(sver)
                if index != -1:
                    if len(ret) == 0:
                        ret = lines[i]
                    else:
                        print("■重複しています。")
    if len(ret) == 0:
        print("見つかりませんでした。")
    return ret


def main(filename, filename2, psp):
    print("■" + filename)
    buf = ''
    with open("testdata\\" + filename, "r", encoding="utf-8") as f:
        buf = f.read()
    json_obj = json.loads(buf)
    
    buf2 = ''
    with open(filename2, "r", encoding="utf-8") as f:
        buf2 = f.read()
    lines = buf2.split('\n')
    
    ret = ""
    
    for test in json_obj:
        #print(test['testNo'])
        #print(test['header']['IV'])
        #print(test['header']['SN'])
        #print(test['header']['Sver'])
        ret += test['testNo'] + "\t" + test['header']['SN'] + "\t" + test['header']['IV'] + "\t" + test['header']['Sver'] + "\t"
        result = check_file(lines, test['header']['IV'], test['header']['SN'], test['header']['Sver'])
        ret += result + "\n"
        #print(result)
    
    with open("result2\\" + psp + ".txt", "w", encoding="utf-8") as f:
        f.write(ret)


if __name__ == '__main__':
    main("ncoms_test.json", "search-results-2025-03-10T00_19_29.550-0700.csv", "ncoms")
    main("nicos-pg_test.json", "search-results-2025-03-10T00_19_29.550-0700.csv", "nicos")
    main("smbc-fs_test.json", "search-results-2025-03-10T00_19_29.550-0700.csv", "smbcfs")
    main("smbc-gp_test.json", "search-results-2025-03-10T00_19_29.550-0700.csv", "smbcgp")
    main("sony_test.json", "search-results-2025-03-10T00_19_29.550-0700.csv", "sony")
    main("veritrans_test.json", "search-results-2025-03-10T00_19_29.550-0700.csv", "dgft")
    main("yamato_test.json", "search-results-2025-03-10T00_19_29.550-0700.csv", "yamato")
    main("zeus_test.json", "search-results-2025-03-10T00_19_29.550-0700.csv", "zeus")
    main("gmo-mb_test.json", "search-results-2025-03-10T00_19_29.550-0700.csv", "gmomb")
    main("gmo-pg_test.json", "search-results-2025-03-10T00_19_29.550-0700.csv", "gmopg")
    main("multi_psp_test.json", "search-results-2025-03-10T00_19_29.550-0700.csv", "multi_psp")
    main("paygent_test.json", "search-results-2025-03-10T00_19_29.550-0700.csv", "paygent")
    main("pay-jp_test.json", "search-results-2025-03-10T00_19_29.550-0700.csv", "pay_jp")
    main("rakuten_test.json", "search-results-2025-03-10T00_19_29.550-0700.csv", "rakuten")
    main("sbps_test.json", "search-results-2025-03-10T00_19_29.550-0700.csv", "sbps")


"""
"""