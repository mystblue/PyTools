# -*- coding: utf-8 -*-
import math
import random
import numpy as np
import time

start = time.time()

n = 13 # ガチャのアイテム数
sn = 41 # 試行回数

print("コンプガチャシミュレート (%d アイテム)" % n)
print("論理値            : {0:.5f}".format(sum([float(n) / i for i in range(1, n+1)])))

ress = []
for j in range(sn):
    box = []
    k = 0
    i = 0
    while(i < n):
        k += 1
        r = random.randrange(n)
        if r not in box:
            i += 1
            box.append(r)
    ress.append(k)
res = np.mean(ress)
print("シミュレーション値: {0:.5f} [{1}回]".format(res, sn))
print("- exec time: %d ms-" % (time.time() * 1000 - start * 1000))
