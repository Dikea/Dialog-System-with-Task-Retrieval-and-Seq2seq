#-*- coding: utf-8 -*-


import re
import random


order_ask_pattern = re.compile(r"订单")


def intent_update(msg, dialog_status):
    if not dialog_status.order_id and dialog_status.user_msg_cnt <= 2:
        prob = random.random()
        if prob < 0.7:
            dialog_status.intent = "orderid_ask"
    return dialog_status


def orderid_ask_handle(msg, dialog_status):
    response = ("麻烦您提供下订单号，妹子帮您查看一下哦，#E-s[数字x]，点击我的订单"
        "-商品左上方-订单编号，复制给我就可以了呢#E-s[数字x]")
    dialog_status.order_id = "[ORRDERID]" 
    return response
