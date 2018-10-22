import re

def intent_update(msg,dialog_status):
    sale_return_keyword = "|".join(["退一下货","退货","退回.*货","货.*要退","退了吗","退吗"])
    if re.search(sale_return_keyword,msg):
        dialog_status.sale_return_intent = True
        dialog_status.intent = "sale_return"

    return dialog_status


# class DialogStatus(object):
    
#     def __init__(self):
#         self.intent = None
#         self.ware_id = None
#         self.order_id = None
#         self.sale_return_intent = None


def sale_return(sentence,dialog_status):
#     """
#     sentence:
#     dialog_status: user history info card slot
    
#     class DialogStatus(object):

#         def __init__(self):
#             self.intent = None
#             self.ware_id = None
#             self.order_id = None
#     """
    order_id = dialog_status.order_id
 
        
    if re.search("不.*喜欢.*退货",sentence):
        return "#E-s[数字x]支持[数字x]天无理由退货，麻烦您提供一下您的订单号，小妹这边会帮您提交退货申请"
    

            
    if re.search("不",sentence):
        if not re.search("不要|不对|可不可以|可以不可以",sentence):return None

    sale_return_keyword = "|".join(["退一下货","退货","退回.*货","货.*要退","退了吗","退吗"])
    #if re.search(sale_return_keyword,sentence) or dialog_status.sale_return_intent:
    if dialog_status.sale_return_intent:
        if not re.search(sale_return_keyword,sentence):
            dialog_status.sale_return_intent = None
            dialog_status.intent = None
        else:
            dialog_status.sale_return_intent = True
            dialog_status.intent = "sale_return"
                
        if re.search("水果|食品",sentence):
            return "您好，食品是不支持[数字x]天无条件退货的"     
            
        if re.search("地址",sentence):return "服务单审核完毕后，系统会自动发短信通知您返回地址。"
        
        if re.search("到付",sentence):return "不可以使用到付的呢，亲"
        
        if re.search("运费|邮费",sentence):
            if re.search("质量",sentence):
                return "您好，如果是质量原因造成的退货，卖家是要报销运费的"
            return "您好，你当时下单的时候，如果勾选了运费险，货物退还后，[数字x]天后运费险会退到您的账户，否则，您需要自己支付退货的邮费。如果是货物质量问题，商家会承担运费的。"
        
        if re.search("赠品",sentence):
            return "您好，申请退货的主商品以及赠品都需要返还销售商"
        
        if re.search("多长时间|多久",sentence):
            return "您好，退货处理自接收到问题商品日期起7日之内处理完成"
        
        if re.search("退货.*处理|退货.*处理",sentence):
            if order_id:return "您好，订单号{}的退货申请小妹已经帮您提交".format(order_id)
            return "请您提供订单号，小妹会帮您处理"
        
        if re.search("进度",sentence):
            #if re.search("查|查询|查看",sentence):
            return "您好，您可以点击我的>退换/售后>进度查询，找到对应的退换货商品，点击右上角“进度查询”，即可查看服务单进度。"
                
        if re.search("如何|怎么|怎样|哪里",sentence):
            if not re.search("怎么样",sentence):
                return "您好，您可以打开京东APP客户端，点击我的>退换/售后>申请售后，填写退换货信息后，即可提交，提交成功后请耐心等待，由专业的售后工作人员受理您的申请。"
        
        if re.search("发货|取消",sentence):
            if re.search("发货",sentence):return "亲爱的，您申请取消的时候如果已经发货了，需要到站点后退回库房退款,您到时候拒收就可以啦"
            if re.search("退货|申请",sentence):
                return "这个无法取消驳回的呢如果需要的话需要您重新下单的哦,如果订购了不需要的单，到货后您拒收就可以啦"
        
        if re.search("退货.*情况|怎么样",sentence):
            if order_id:return "您好，您的订单号为{}的退货申请已经通过，等货物回到库房，会给您退款".format(order_id)
            return "您好，您的退货申请已经通过，等货物回到库房，会给您退款"
    
        if re.search("可以.*[么嘛吗]|行.*[么嘛吗]|可否",sentence):
            if order_id:return "您好，是可以的。请问是{}这个订单号的物品吗？如果是的话，小妹这边帮您提交申请".format(order_id)
            return "您好，是可以的，麻烦您提供一下您的订单号，小妹这边会帮您提交申请"
    
        if re.search("退一下货|给.*退|帮.*退|要退货|想退货|退货吧|申请退货|要求退货|需要退货|处理.*退货",sentence):
            if not re.search("[嘛么吗]",sentence):
                if order_id:return "您好，请问是{}这个订单号的物品吗？如果是的话，小妹这边帮您提交申请".format(order_id)
                return "麻烦您提供一下您的订单号，小妹这边会帮您提交退货申请"
        
        if re.search("退回|退款|到账",sentence):
#             if re.search("没有|未",sentence):
#                 return 
            if order_id:return "您好，您之前{}的订单商品退回仓库之后，会给您安排退款的".format(order_id)
            return "商品退回仓库之后，会给您安排退款的"
        
        if re.search("什么时[候间]",sentence):
            if re.search("取件",sentence):
                return "请您稍等一下正在为您核实处理中哦,[数字x][数字x]天内取件"
            return "亲爱的[时间x]前提交的单我们会在当天[时间x]前审核完毕[时间x]后提交的单我们会在次日[时间x]前会审核完毕#E-s[数字x]#E-s[数字x]，请您放心呀小妹跟您保证我们会尽快为您审核处理哒#E-s[数字x]"
        

        if re.search("怎么退货|哪.*退货",sentence):
            if not re.search("了",sentence):
                return "您好您可以在【个人中心客户服务售后申请】提交售后申请，提交了京东自营的返修退换货当天[时间x]之前提交的返修单在当天[数字x]点之前会有人员审核，[时间x]之后提交的返修单次日[时间x]之前会有人员审核给您审核处理的，具体以审核意见为准，到时候您按照审核意见处理就可以了呢#E-s[数字x]"
          
        if re.search("安排",sentence):
            return "您好，您的取消申请已提交"
        
        if order_id:return "您好，订单号{}的退货申请小妹已经帮您提交".format(order_id)


    return None
