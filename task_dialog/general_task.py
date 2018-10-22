#-*- coding: utf-8 -*-


import re


def intent_update(msg, dialog_status):
    if re.search(r"怎|如何|要|哪", msg):
        dialog_status.intent = "general"
    return dialog_status


def general_handle(msg, dialog_status):

    if re.search(r"怎|如何|要|哪", msg):
        # Order comment related.
        if re.search(r"(?=.*删)(?=.*(评[价论]|晒单))", msg):
            return ("亲，商品评价或晒单在发布之后，用户是无法修改、删除晒单或评价的。")
        if re.search(r"(?=.*改)(?=.*评[价论])", msg):
            return ("评价是无法修改的呢，如果要追加建议您追评说明一下")
        if re.search(r"(?=.*查看)(?=.*(评[价论]|晒单))", msg):
            return ("亲，进入商品详情页面，点击页面中的“商品评价”，在商品评价页面点击“有晒单的评价”即可查看呢")
        if re.search(r"(?=.*(晒单|订单))(?=.*评[价论])", msg):
            return ("亲爱哒，评价晒单操作，登陆京东--我的订单--“评价”/“晒单”")
        if re.search(r"(?=.*(晒单|订单))(?=.*评[价论])(?=.*好处)", msg):
            return ("亲爱哒，评价晒单成功后，您能够得到相应的京豆奖励哦")


    return None 


if __name__ == "__main__":
    print (general_handle("怎么查看自己的评价呢", None))
    print (general_handle("去哪里可以删除订单的评价呢", None))
