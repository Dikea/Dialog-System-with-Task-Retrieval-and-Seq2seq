#-*- coding: utf-8 -*-


import re


def log_print(text, level="DEBUG"):
    print ("[%s] %s" % (level, text))


ch_pattern = re.compile(r"[\u4e00-\u9fa5]+")
remove_pattern = re.compile(r"好的")

def ch_count(text):
    # Count chinese number.
    text = remove_pattern.sub("", text)
    r = ch_pattern.findall(text)
    cnt = len("".join(r))
    return cnt
