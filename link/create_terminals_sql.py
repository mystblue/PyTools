# encoding: utf-8

"""
"""

import os

file_path = "terminal_test_data.sql"

def main():
    book_list = []
    with open(file_path, "w", encoding="cp932", newline="\n") as fw:
        for i in range(10000):
            ret = "INSERT INTO terminals(created, modified, create_user_id, modify_user_id, enable, status, sn, credit_terminal_no, terminal_app_set_id, terminal_pass, pairing_pass, merchant_id, reboot_timeout, note, pay_tg_url_id) VALUES ('2024-04-17 17:05:00', '2024-04-17 17:05:00', 0, 0, 1, 2, 'TEST240417" + "{:05d}".format(i + 1) + "', '', 5, '', '', [加盟店ID], 0, '', 11);"
            fw.write(ret)
            fw.write('\n')

if __name__ == '__main__':
    main()