# -*- coding: utf-8 -*-

import json
import re

is_debug = True
#is_debug = False

HTML = """<!doctype html>
<html>
<head>
    <title>{0}</title>
    <style type="text/css">
	body {{
		margin: auto 10%;
		/*color: #333333;*/
        color: #4a4a4a;
        background: radial-gradient(snow, whitesmoke);
        line-height: 150%;
	}}
    span.topic {{
        font-weight: bold;
        color: #555555;
    }}
    h2 {{
        font-size: 1.1em;
        color: royalblue;
        margin-top: 0px;
        border-bottom: 1px dotted gainsboro;
    }}
    h2.old {{
        display: inline-block;
        /*border-bottom: solid 3px blue;*/
        /*border-left: solid 5px #7db4e6;*/
        border-bottom: dotted 1px #7db4e6;
        /*padding: 0.25em 0.5em;*/
        padding-bottom: 2px;
        margin-bottom: 0.2em;
        color: #494949;
    }}
    
    h3 {{
        font-size: 1.05em;
        margin-block-start: 1em;
        margin-block-end: 1em;
        margin-inline-start: 0px;
        margin-inline-end: 0px;
        font-weight: bold;
        color: olive;
    }}
    
    div.toc {{
        border: 1px dotted silver;
        padding: 1em;
        margin-top: 1em;
        margin-bottom: 2em;
        border-radius: 3px;
        background-color: white;
    }}
    
    div.card {{
        border: 1px solid gainsboro;
        box-shadow: 0 0.5em 1em -0.125em rgb(10 10 10 / 10%), 0 0 0 1px rgb(10 10 10 / 2%);
        padding: 0.8em;
        margin-bottom: 2em;
        border-radius: 3px;
        background-color: white;
        border-radius: 10px;
    }}
    p {{
        margin-block-end: 0.5em;
    }}
    ul.toc {{
        margin: 0px;
    }}
    table {{
        border-right: 1px solid silver;
        border-bottom: 1px solid silver;
        border-spacing: 0px;
    }}
    th, td {{
        border-top: 1px solid silver;
        border-left: 1px solid silver;
        padding: 5px;
        min-width: 50px;
    }}
	a:link {{
	   color: blue;
	   text-decoration: none;
	}}
	a:visited {{
	   color: blue;
	   text-decoration: none;
	}}
	a:hover {{
	   color: purple;
	}}
	a:active {{
	   color: purple;
	}}
    </style>
</head>
<body>
{1}
</body>
</html>"""

class IndexRender:

    text = ""

    def __init__(self, reader):
        self.reader = reader

    def create_html(self, title):
        json_obj = self.reader.get_json_obj()
        body = "<ul>"
        for item in json_obj:
            body = body + "<li><a href=\"" + item["name"] + ".html\">" + item["name_ja"] + "</a></li>"
            if "sub" in item:
                body = body + "<ul>"
                for sub_item in item["sub"]:
                    body = body + "<li><a href=\"" + sub_item["name"] + ".html\">" + sub_item["name_ja"] + "</a></li>"
                body = body + "</ul>"
        body = body + "</ul>"
        self.text = HTML.format(title, body)
    def write(self, dst):
        with open(dst, 'w', encoding="utf-8") as f:
            f.write(self.text)

class JsonReader:
    json_obj = None
    def read_json(self, src):
        json_open = open(src, 'r', encoding='utf-8')
        self.json_obj = json.load(json_open)

    def get_json_obj(self):
        return self.json_obj

# ブロッククラス
class Block:
    title = ""
    date = ""
    tag = None
    last = None
    def __init__(self):
        self.contents = []
    
    def add(self, line):
        if line.startswith("|"):
            self.change_table()
        else:
            self.change_paragraph()
        self.last.add(line)

    def change_table(self):
        if type(self.last) != Table:
            self.last = Table()
            self.contents.append(self.last)

    def change_paragraph(self):
        if type(self.last) != Paragraph:
            self.last = Paragraph()
            self.contents.append(self.last)

    def print(self):
        for item in self.contents:
            print(item.output_html())

class Paragraph:
    def __init__(self):
        self.contents = []

    def add(self, line):
        pattern = re.compile(r'\[([^\]]+)\]\(([^\)]+)\)')
        line = pattern.sub(r'<a href="\2" target="_blank">\1</a>', line)
        line = line.replace('[ ]', '<input type="checkbox" class="task-list-item-checkbox" disabled="">')
        line = line.replace('[x]', '<input type="checkbox" class="task-list-item-checkbox" checked="" disabled="">')
        if line.startswith("## "):
            line = "<h3>" + line[3:] + "</h3>"
        self.contents.append(line)

    def output_html(self):
        ret = ""
        if self.contents[-1] == '':
            self.contents.pop()
        for line in self.contents:
            ret = ret + "<p>" + line + "</p>"
        print(ret)
        return ret

class Table:
    def __init__(self):
        self.contents = []

    def add(self, line):
        self.contents.append(line)

    def output_html(self):
        ret = "<table>"
        for line in self.contents:
            ret += "<tr>"
            splitted = line.split("|")
            splitted.pop(0)
            splitted.pop()
            for item in splitted:
                if item.startswith("_."):
                    ret += "<th>" + item[2:] + "</th>"
                else:
                    ret += "<td>" + item + "</td>"
            ret += "</tr>"
        ret += "</table>"
        print(ret)
        return ret

# Markdown パーサー
class MarkdownParser:
    title = ""
    block_list = None
    
    def read_file(self, src):
        str = ""
        with open(src, "r", encoding="utf-8") as f:
            str = f.read()
        return str

    def parse_str(self, str):
        # 行分割
        lines = str.splitlines()
        
        block_list = list()

        last_block = None
        for i in range(len(lines)):
            if i == 0 and lines[i].startswith("Title:"):
                self.title = lines[i][6:].lstrip()
                continue
            if lines[i] == '':
                if last_block and len(last_block.contents) > 0:
                    last_block.add("")
                continue
            line = lines[i].lstrip()
            
            if line.startswith("# "):
                block = Block()
                block.title = line[2:]
                block_list.append(block)
                last_block = block
            elif line.startswith("TAG:"):
                str = lines[i][4:].lstrip()
                tags = str.split(',')
                tag_list = list()
                for tag in tags:
                    tag_list.append(tag)
                last_block.tag = tag_list
            elif line.startswith("DATE:"):
                last_block.DATE = lines[i][5:].lstrip()
            else:
                last_block.add(line)
        
        return block_list

    def parse(self, src):
        # ファイルを読み込む
        str = self.read_file(src)
        # 仕様書をパースする
        self.block_list = self.parse_str(str)

    def get_block_list(self):
        return self.block_list

    def write(self, dst):
        with open(dst, 'w', encoding="utf-8") as f:
            json.dump(self.test_data, f, ensure_ascii=False, indent=4)

    def print(self):
        for block in self.block_list:
            print(block.title)
            print("----------")
            block.print()
            print("----------")
	
class HtmlRenderer:
    json_obj = None
    block_list = None
    html = ""

    def __init__(self, json_obj, block_list):
        self.json_obj = json_obj
        self.block_list = block_list

    def write(self, html, dst):
        with open(dst, 'w', encoding="utf-8") as f:
            f.write(html)

    def convert_markdown(self, contents):
        ret = ""
        for obj in contents:
            if type(obj) == Paragraph:
                ret = ret + obj.output_html()
            if type(obj) == Table:
                ret = ret + obj.output_html()
        return ret

    def create_html(self, out_list):
        body = ""
        for item in out_list:
            if type(item) is Block:
                body = body + "<div class=\"card\">"
                body = body + "<h2 id=\"" + item.title + "\">" + item.title + "</h2>"
                print(item.contents)
                body = body + self.convert_markdown(item.contents)
                body = body + "</div>"
        return body

    def create_toc(self, out_list):
        """目次を生成する"""
        ret = "<div class=\"toc\">目次<ul class=\"toc\">"
        for item in out_list:
            ret = ret + "<li><a href=\"#" + item.title + "\">" + item.title + "</a></li>"
        ret = ret + "</ul></div>"
        return ret

    def output_tag(self, tag):
        out_list = list()
        for block in self.block_list:
            if tag in block.tag:
                out_list.append(block)
        # ソートする
        out_list.sort(key=lambda x: x.title, reverse=False)
        # 降順
        #out_list.sort(key=lambda x: x.title, reverse=True)
        html = self.create_html(out_list)
        
        toc = self.create_toc(out_list)
        
        html = HTML.format("", toc + html)
        self.write(html, "..\\" + tag + ".html")

    def output(self):
        """tag.json の各タグを出力する
        """
        for item in self.json_obj:
            self.output_tag(item["name"])
            if "sub" in item:
                for sub_item in item["sub"]:
                    self.output_tag(sub_item["name"])

    def output_tag_debug(self, tag):
        out_list = list()
        for block in self.block_list:
            if tag in block.tag:
                out_list.append(block)
        # ソートする
        out_list.sort(key=lambda x: x.title, reverse=False)
        # 降順
        for out in out_list:
            print(out)
            print(out.title)
            print(out.contents)

    def output_debug(self):
        """tag.json の各タグを出力する
        """
        for item in self.json_obj:
            self.output_tag_debug(item["name"])

def create_html(json_file, src):
    reader = JsonReader()
    reader.read_json(json_file)
    parser = MarkdownParser()
    parser.parse(src)
    render = HtmlRenderer(reader.get_json_obj(), parser.get_block_list())
    render.output()
    irender = IndexRender(reader)
    irender.create_html(parser.title)
    irender.write("..\\index.html")

def debug_markdown_parser(src):
    parser = MarkdownParser()
    parser.parse(src)
    parser.print()

def debug_html_renderer(json_file, src):
    reader = JsonReader()
    reader.read_json(json_file)
    parser = MarkdownParser()
    parser.parse(src)
    render = HtmlRenderer(reader.get_json_obj(), parser.get_block_list())
    render.output_debug()

if __name__ == '__main__':
    create_html('tag.json', 'kuro.md')
    #debug_markdown_parser('persona3r.md')
    #debug_html_renderer('tag.json', 'persona3r.md')


"""
"""