#-*- coding: utf-8 -*-


import codecs
import jieba


with codecs.open("total_ware.txt", "r", "utf-8") as  rfd:
    for line in rfd:
        line = line.strip().replace("/", " ")
        tokens = jieba.lcut_for_search(line)
        for w in tokens:
            if len(w) > 1:
                print (w)
