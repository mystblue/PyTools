import os
import os.path
import requests
from bs4 import BeautifulSoup

PATH = "C:\\Users\\314\\Documents\\git\\PyTools\\novel\\kage"

def get(num):
    url = "https://ncode.syosetu.com/n0611em/{0}/".format(num)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    print(response.status_code)

    print(response.text)

    with open(os.path.join(PATH, "{0}.html".format(num)), "w", encoding="utf-8") as f:
        f.write(response.text)

def parse(num):
    with open(os.path.join(PATH, "{0}.html".format(num)), "r", encoding="utf-8") as f:
        buf = f.read()
    soup = BeautifulSoup(buf, "html.parser")

    title = soup.find('h1', class_='p-novel__title p-novel__title--rensai')

    mainTag = soup.find('div', class_='js-novel-text p-novel__text')

    ret = "## " + title.text + "\n\n"
    for p in mainTag:
        if p.name == 'p':
            #print("「" + p.text + "」")
            text = p.text
            if p.text.startswith("　"):
                text = text[1:]
            if text.endswith(" "):
                text = text[:-1]
            ret += text + "\n"
    return ret

def save(text, num):
    with open(os.path.join(PATH, "{0}.txt".format(num)), "w", encoding="utf-8") as f:
        f.write(text)

if __name__ == '__main__':
    path = os.getcwd()

    for i in range(4, 23):
        num = str(i)
        get(num)
        text = parse(num)
        save(text, num)