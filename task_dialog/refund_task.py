import re

def intent_update(msg,dialog_status):    
    sign = "(?=.*[钱款])(?=.*退)|[差保降]价|价保"
    if re.search(sign,msg):
        dialog_status.intent = "refund"

    return dialog_status

def refund_response(sentence,dialog_status):
    if re.search("不.*喜欢.*退[钱款]",sentence):
        return "麻烦您提供一下您的订单号，小妹这边会帮您提交退货申请"
    order_id = dialog_status.order_id
    
    if re.search("不",sentence):
        if not re.search("不要|不对|可不可以|可以不可以",sentence):return None
    
    sign = "(?=.*[钱款])(?=.*退)|[差保降]价|价保"
#     
    if True:
        if not re.search(sign, sentence):
            if dialog_status.intent == "refund":
                dialog_status.intent = None
        
        if re.search("水果|食品",sentence):
            return "您好，食品是不支持[数字x]天无条件退货的"
        
        if re.search("保价|差价|降价|价保",sentence): 
            if order_id:return "您好，订单号{}的申请已经提交，财务正在处理，这个价保退款是[数字x][数字x]个工作日退还到您原支付账户,请您耐心等待".format(order_id)
            if re.search("进度|情况",sentence):
                return "#E-s[数字x]价保[金额x][日期x][时间x]原返哈您当时怎么支付的就退到哪里去哈"
            
            return "您好，请您提供一下订单号，小妹这边帮您查询。ps:差价是有补偿的。审核通过后，会在[数字x][数]个工作日退还到您原支付账户的，登录电脑端:我的京东-客户服务-价格保护;手机端:我的-客户服务-价格保护可以查看申请和价保的具体审核情况哦"
        
        if re.search("审核",sentence):
            return "您好,请您耐心等候，商家审核通过后，退款会退还到您原支付账户的"
        
        if re.search("重新拍|重新下单|重新下了单|再下单|重新买|再买",sentence):
            return "好的,先给您退了,然后您在重新购买就可以啦"
        
        if re.search(r"取消退款|取消申请|取消申请|撤销申请", sentence):
            return "订单一旦取消无法恢复的呢，系统正在拦截的呢，如果拦截未成功，会继续配送，后期配送到了您可以签收的呢"
        
        if re.search("退款申请|退钱申请",sentence):
            if re.search("尽快",sentence):return "您好，退款申请一般签收后是[数字x]小时审核的呢"
            if re.search("多久|什么时间|什么时候|多长时间",sentence):return "您好，具体退款周期还请您查看：URL，如您的订单退款超过退款周期仍未收到退款，请您联系客服进行处理。"
            if re.search("取消|撤销", sentence):return "订单一旦取消无法恢复的呢"
                
        if re.search("进度|情况",sentence):
            if order_id:return "您好，您的订单号{}的申请财务正在处理中，退款是[数字x][数字x]个工作日退还到您原支付账户的，请您耐心等待".format(order_id)
            return "您可以登陆京东，进入“我的订单”-“客户服务”-“返修/退换货”页面；点击“查看退款记录”，查看退款明细"
        
        if re.search("可以.*[么嘛吗]|行.*[么嘛吗]|可否",sentence):
            if re.search(sign,sentence):
                return "亲，请您提供订单号，小妹这边帮您提交申请，等待财务审核通过以后就可以返回了"
        
        if re.search("[钱款].*退[到回]|[钱款]退.*哪[儿里]|没到账|退多少",sentence):
            return "您好，退款原返哦，支付金额会退还到您原支付账户的,请您耐心等候"
        
        if re.search("查[询看]",sentence):
            if re.search("想|帮|怎么|怎样|如何|要",sentence):
                return "您可以登陆京东，进入“我的订单”-“客户服务”-“返修/退换货”页面；点击“查看退款记录”，查看退款明细"
            if re.search("退款查询|查询退款",sentence):
                return "您可以登陆京东，进入“我的订单”-“客户服务”-“返修/退换货”页面；点击“查看退款记录”，查看退款明细"

        if re.search("尽快|多久|周期|何时|什么时候|什么时间|啥时|何时|到账", sentence):
            if re.search("银行|储蓄卡", sentence):
                return "储蓄卡[数字x]-[数字x]工作日到账(具体以银行信息为准哦)。还请您耐心等待银行短信通知，谢谢"
            if re.search("信用卡", sentence):
                return "信用卡[数字x]-[数字x]DIGIT工作日到账。还请您耐心等待银行短信通知，谢谢"
            if re.search("微信", sentence):
                return "微信零钱[数字x]-[数字x]工作日到账。还请您注意查收，如果超期没有退款，您再联系我们帮您处理下的，谢谢"
            if re.search("余额|京豆|京东卡|可返还的优惠券", sentence):
                return "余额/京豆/京东卡/可返还的优惠券[数字x]小时到账~。还请您注意查收，如果超期没有退款，您再联系我们帮您处理下的，谢谢"
            if re.search("白条", sentence):
                return "白条是[数字x]-[数字x]DIGIT个工作日退款到账或恢复额度。还请您注意查收，如果超期没有退款，您再联系我们帮您处理下的，谢谢"
        
            return "您好，退款是[数字x][数字x]个工作日退还到您原支付账户的，还请您耐心等待"
            
        if re.search("怎么|帮.*退[钱款]|如何|要退[款钱]|想退[款钱]|退[款钱]吧|申请退[款钱]|要求退[款钱]|需要退[款钱]|处理.*退[款钱]",sentence):
            if order_id:return "您好，请问是{}这个订单号的物品吗？如果是的话，小妹这边帮您提交申请".format(order_id)
            return "麻烦您提供一下您的订单号，小妹这边会帮您提交退货申请"

        if order_id:return "您好，订单号{}的退款申请已经提交，财务正在进行退款审核，退款是[数字x][数字x]个工作日退还到您原支付账户的，请您耐心等待".format(order_id)
    
    return None

# # -*- coding:utf-8 -*-
# import re
# import random 

# def intent_update(msg,dialog_status):    
#     refund_keyword = "|".join(["退款","退钱","[保差降]价","价保","钱","款"])
#     if re.search(refund_keyword, msg):
#         dialog_status.intent = "refund"

#     return dialog_status


# def refund_response(sentence, dialog_status):        
#     if re.search(r"不.*喜欢.*退[款钱]|想.*退[款钱]|要.*退[款钱]|能.*退[款钱]|可以.*退[款钱]",sentence):
#         return "商品如果不存在质量问题不可以退款哦，若是质量问题，请您提供订单号，小妹帮您提交申请，等待财务审核通过以后就可以返回了"
            
#     refund_keyword = "|".join(["退款","退钱","[保差降]价","价保","钱","款"])
  
#     if dialog_status.intent == "refund":
#         if not re.search(refund_keyword, sentence):
#             dialog_status.intent = None
        
#         if re.search(r"ORDER",sentence):
#             if dialog_status.order_id:return "您好，订单号{}的退款申请小妹已经帮您提交".format(dialog_status.order_id)
            
#         if re.search(r"(?=.*(怎么|如何))(?=.*查询)", sentence):
#             return "您可以登陆京东，进入“我的订单”-“客户服务”-“返修/退换货”页面；点击“查看退款记录”，查看退款明细"
        
#         if re.search(r"哪[里儿]", sentence):
#             return "退款原返哦，怎么支付怎么退回"
        
#         if re.search(r"取消申请|不退|撤销申请|关闭", sentence):
#             return "订单一旦取消无法恢复的呢，系统正在拦截的呢，如果拦截未成功，会继续配送，后期配送到了您可以签收的呢"
       
#         if re.search("进度|情况", sentence):
#             if random.randint(1,2) == 1:
#                 return "您的订单已出库，系统会尽力拦截不发货，万一后续发到了烦请拒收，待商品退库受理退款哦#E-s[数字x]"
#             else:
#                 return "您的订单拦截成功，财务正在进行退款审核，请耐心等待"
            
#         if re.search("多久|周期|何时|什么时候|时间|退款|退钱|钱|款|为什么|为啥|啥时候", sentence):
#             return "这边显示正在处理中，小妹为您解释一下哦，您的订单申请取消后，要先等待商品退回商家的，商家收到商品后会发起退款申请，申请审核通过订单删除后，会给您及时退款，白条是[数字x]-[数字x]DIGIT个工作日退款到账或恢复额度，微信零钱[数字x]-[数字x]工作日到账，储蓄卡[数字x]-[数字x]工作日到账(具体以银行信息为准哦)，信用卡[数字x]-[数字x]DIGIT工作日到账;余额/京豆/京东卡/可返还的优惠券[数字x]小时到账~ 还请您注意查收，如果超期没有退款，您再联系我们帮您处理下的，谢谢"
            
#         if re.search("银行|储蓄卡", sentence):
#             return "这边显示正在处理中，储蓄卡[数字x]-[数字x]工作日到账(具体以银行信息为准哦)。还请您耐心等待银行短信通知，谢谢"
#         if re.search("信用卡", sentence):
#             return "这边显示正在处理中，信用卡[数字x]-[数字x]DIGIT工作日到账。还请您耐心等待银行短信通知，谢谢"
#         if re.search("微信", sentence):
#             return "这边显示正在处理中，微信零钱[数字x]-[数字x]工作日到账。还请您注意查收，如果超期没有退款，您再联系我们帮您处理下的，谢谢"
#         if re.search("余额|京豆|京东卡|可返还的优惠券", sentence):
#             return "这边显示正在处理中，余额/京豆/京东卡/可返还的优惠券[数字x]小时到账~。还请您注意查收，如果超期没有退款，您再联系我们帮您处理下的，谢谢"
#         if re.search("白条", sentence):
#             return "这边显示正在处理中中，白条是[数字x]-[数字x]DIGIT个工作日退款到账或恢复额度。还请您注意查收，如果超期没有退款，您再联系我们帮您处理下的，谢谢"
#         if re.search("[保差降]价|价保", sentence):
#             if re.search("什么", sentence):
#                 return "就是对您购买商品后，商品又降价的差额退款呢，符合规则的话，应价保[价保金额(单件)] * [价保商品数量] = [金额x]，是原路返还的"
#             return "差价是有补偿的。审核通过后，会在[数字x][数]个工作日退还到您原支付账户的，登录电脑端:我的京东-客户服务-价格保护;手机端:我的-客户服务-价格保护可以查看申请和价保的具体审核情况哦"
     
        
#     return None
