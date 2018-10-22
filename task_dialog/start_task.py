#-*-coding:utf-8-*-


import re
import random
from utils.tools import ch_count


not_match_pattern = re.compile(r"吗|\?|？|多|哪|怎|什么|啥|退|发票")
start_pattern = re.compile(
    r"http|"
    r"您好|"
    r"你好|"
    r"在|"
    r"那个|"
    r"有人|"
    r"转人工|"
    r"hi|"
    r"(?=.*咨询)(?=.*订单)")


def intent_update(msg, dialog_status):  
    if (ch_count(msg) <= 8 
        and not not_match_pattern.search(msg)
        and len(dialog_status.context) == 1 
        and start_pattern.search(msg)
        and not dialog_status.start_flag):
        dialog_status.intent = "start"
        dialog_status.start_flag = True
    return dialog_status


def start_handle(sentence,dialog_status):
    greeting_sheet = [
        "您好小主，在的哈，美好的一天从遇见您开始，请问有什么可以为您服务的呢(^_^)", 
        "您好，有什么问题我可以帮您处理或解决呢(^_^)", 
        "亲，请问有什么可以帮助您呢 ^_^", 
        "亲爱哒，小妹在的呢，有什么需要帮助的呢#E-s[数字x](^_^)", 
        "亲，有缘又相见了，有什么是我可以帮您的呢(^_^)"]
    response = random.sample(greeting_sheet, 1)[0]
    return response
