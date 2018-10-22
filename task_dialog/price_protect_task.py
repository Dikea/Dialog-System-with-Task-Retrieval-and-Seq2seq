#-*- coding: utf-8 -*-


import re


price_protect_pattern = re.compile(r"(?=.*价)(?=.*(降|保))")


def intent_update(msg, dialog_status):
    if price_protect_pattern.search(msg):
        if not "没有" in msg:
            dialog_status.intent = "price_protect"
    return dialog_status 


def price_protect_handle(msg, dialog_status):
    if "周期" in msg:
        dialog_status.intent = None
        return ("https://help.jd.com/user/issue/[数字x]-[链接x]，这个是我们的价保商品的时间，您可以看下哦")
    if not dialog_status.order_id:
        dialog_status.order_id = "[ORDERID_数字x]"
        return ("还请您提供下订单号可以吗~ 妹子为您查询的呢")
    elif not dialog_status.price_protect_success:
        dialog_status.price_protect_success = True
        return ("好的，妹纸帮您申请价保成功了呢，补您差价[数字x]元，预计[数字x]-[数字x]"
            "个工作日到账哦，款项是原返的哦，请问还有其他还可以帮到您的吗?#E-s[数字x]")
    return None
