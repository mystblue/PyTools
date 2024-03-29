# encoding: utf-8

"""
"""

file_path = "sql.txt"

def main():
    buf = "insert into receipt (created, modified, create_user_id, modify_user_id, receipt_name) values ('2024-03-29 14:58:50', '2024-03-29 14:58:50', 70, 0, 'test{}');\n"
    with open(file_path, "w", encoding="utf-8") as fw:
       for i in range(45):
           count = i + 2
           fw.write(buf.format(count, count, count))

if __name__ == '__main__':
    main()