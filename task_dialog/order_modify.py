#-*-coding:utf-8-*-


import re


order_modify_pattern = re.compile(
    r"(?=.*(改|错))(?=.*单)")


def intent_update(msg, dialog_status):
    if order_modify_pattern.search(msg):
        dialog_status.intent = "order_modify"
    return dialog_status


def order_modify_handle(msg, dialog_status):
    response = ("您好，正常情况下订单提交成功是不支持修改的呢，麻烦您看下订单详情页是否有“修改”的按钮，如有，"
        "您可点击修改末级地址/联系人/电话号码/送货时间信息，如没有修改按钮，说明订单已不支持修改了呢，还请您理解哦~") 

    if re.search("预售",msg):return "您好，预售商品下单成功之后无法修改订单。"
    if re.search("配送时间",msg):return "您好，京东自营且京东配送（非自提）的在订单打印完成之间均可修改配送时间"
    if re.search("支付",msg):return "您好，支付方式目前是没法修改的"
        
    return response
