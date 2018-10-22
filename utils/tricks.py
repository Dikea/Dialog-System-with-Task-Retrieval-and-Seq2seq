#-*- coding: utf-8 -*-


import codecs
import random
from utils.global_names import GlobalNames, get_file_path


def modify_tokens(tokens):
    new_tokens = []
    pos = 0
    len_ = len(tokens)
    while pos < len_:
        if tokens[pos] == "[":
            if pos+2 < len_ and tokens[pos+2] == "]":
                token = "".join(tokens[pos:pos+3])
                new_tokens.append(token)
                pos += 3
            elif pos+3 < len_ and tokens[pos+3] == "]":
                if tokens[pos+2].isdigit():
                    tokens[pos+2] = "_digit_"
                token = "".join(tokens[pos:pos+4])
                new_tokens.append(token)
                pos += 4
            else:
                pos += 1
        else:
            new_tokens.append(tokens[pos])
            pos += 1
    return new_tokens


def length_weight(corpus, orders, length_limit=6):
    for idx, _ in enumerate(orders):
        if len(corpus[idx]) > length_limit:
            return idx
    return 0
