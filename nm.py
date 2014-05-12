# encoding: utf-8

import re

ubuf = ""
with open("test.html", "r") as frp:
    buf = frp.read()
    ubuf = buf.decode("utf-8")
    ubuf = re.sub("&gt;", ">", ubuf)
    ubuf = re.sub("[ ]+$", "", ubuf)
    ubuf = re.sub("<[^>]+>", "", ubuf)
with open("test.html", "w") as frp:
    frp.write(ubuf.encode("utf-8"))
