import re

def intent_update(msg,dialog_status):
    sign = "|".join(["查询","查查","查一下","问一下","询问","咨询"])
    if re.search(sign,msg):
        dialog_status.query_intent = True
        dialog_status.intent = "query"
    else:
        dialog_status.query_intent = False
        if dialog_status.intent == "query":
            dialog_status.intent = None
    return dialog_status


# class DialogStatus(object):
    
#     def __init__(self):
#         self.intent = None
#         self.ware_id = None
#         self.order_id = None
        
#         self.sale_return_intent = None
#         self.query_intent = None


def query_judge(sentence,dialog_status):
    if "不" in sentence:
        return None
    
    order_id = dialog_status.order_id
    #发票关键词包括了  发票 电子发票 纸质发票  增值税发票 增税发票
    sign = "|".join(["查询","咨询"])
#     if re.search(sign,sentence):
    if True:
        if re.search("物流|配送|到哪",sentence):
            return "亲爱的，登陆[链接x]输入运单号即可查询物流信息哦"
            
        if re.search("快递|订单",sentence):
            if re.search("哪儿",sentence):return "您好，登陆[链接x]输入运单号即可查询物流信息哦"
            if re.search("价格",sentence):return "价格为[数字x]元哦"
            if re.search("取消",sentence):
                if research("怎么|如何",sentence):return "登陆京东app客户端，点击页面右下方【我的】，进入【我的订单】页面查看即可" 
                return "您好，如果您需要取消，小妹这边可以帮您提交申请的哦"
            #return "您好，有什么我可以帮您处理或解决呢"
        
        if re.search("订单号|ORDERID_DIGIT|商品",sentence):
            if re.search("改",sentence):return  "您好，请问您有什么需要修改的呢"
            return "您好请问有什么可以为您效劳#E-s[数字x]"
        
        if re.search("差价",sentence):
            return "您请从新提交个订单,原订单不需要您付款,把生成的新的订单号提供给妹子就可以了哦"
        
        if re.search("取消.*订单",sentence):
            return "好的呢，亲"
        
        if re.search("怎么[咨查]询",sentence):
            return "金融在线客服链接[数字x][数字x]如浏览器无人回应请更换浏览器哦金融[数字x]金融在线客服链接[数字x][数字x]DIGIT[数字x]DIGIT点击后需要重新登录京东账户哦上面都能联系到呢"
        
        if re.search("咨询产品",sentence):
            return "您好，请问您有什么想咨询的呢"
        
        if re.search("满减订单",sentence):
            return "您好，如果您购买了满减的商品需要退换货时，以您这个商品实际支付的金额处理"
    return None
