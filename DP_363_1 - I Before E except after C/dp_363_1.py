#!/usr/bin/env python3

import re


def check(word):
    return bool(re.search('[^c]ei|cie|^ei', word))

print()


with open("enable1.txt") as f:
    cnt = 0
    for line in f:
        cnt = cnt + check(line)

    print(f"Number of matches: {cnt}")
    
    dsum = 0
    while cnt > 0:
        dsum = dsum + cnt % 10
        cnt = cnt // 10
    print(f"The sum of digits: {dsum}")
    print()
