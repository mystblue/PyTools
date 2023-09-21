# -*- coding: utf-8 -*-

import os
import sys

def check_number(digits):
    _sum = 0
    alt = False
    for dg in reversed(digits):
        d = int(dg)
        assert 0 <= d <= 9
        if alt:
            d *= 2
            if d > 9:
                d -= 9
        _sum += d
        alt = not alt
    return (_sum % 10) == 0


print(check_number('4111111111111111'))
print(check_number('1111111111111111'))
