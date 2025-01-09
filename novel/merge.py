import glob  

num = 4

JS_TEMPLATE = """var key = "kage_{0}";
var data = `# 陰の実力者になりたくて！ 第{0}章

{1}
`;""";

PATH = "C:\\Users\\314\\Documents\\git\\PyTools\\novel\\kage{0}\\*.txt".format(num)
OUTPUT = "C:\\Users\\314\\Documents\\git\\PyTools\\novel\\kage_{0}.txt".format(num)
JS_FILE = "C:\\Users\\314\\Documents\\git\\PyTools\\novel\\kage_{0}.js".format(num)

txt_files = glob.glob(PATH) ##拡張子が「*txt」だけのファイルを返す

print(type(txt_files))

ret = ""
for file in txt_files:  
    print(file)
    with open(file, "r", encoding="utf-8") as f:
        ret += f.read()

with open(OUTPUT, "w", encoding="utf-8") as fw:
    fw.write(ret)

with open(JS_FILE, "w", encoding="utf-8") as fw:
    fw.write(JS_TEMPLATE.format(num, ret))
