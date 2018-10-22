#-*- coding: utf-8 -*-
import re

# class DialogStatus(object):
    
#     def __init__(self):
#         self.intent = None
#         self.ware_id = None
#         self.order_id = None
#         self.sale_return_intent = None
        
        
#         self.invoice_intent = False


def intent_update(msg,dialog_status):
    keyword = "|".join(["发票","报销凭证","专票","增票"])
    if re.search(keyword,msg):
        dialog_status.intent = "invoice"
    return dialog_status


def invoice_handle(context, dialog_status):
    #sentence = " ".join(context[::2])
    sentence = context
    invoice_keyword = "|".join(["发票","报销凭证","专票","增票"])
    if dialog_status.intent == "invoice":
        answer1 = invoice_judge(sentence)
        answer2 = invoiceReviseRule(sentence)
        if answer1 or answer2:
            if answer2:return answer2
            if answer1:return answer1
    if not re.search(invoice_keyword,sentence):
        if dialog_status.intent == "invoice":
            dialog_status.intent = None

    return None


def invoice_judge(sentence):
    if "不|没" in sentence:
        if not re.search("不一致|不一样|不同|不对|不太对|不能|不可以|没法|没到|没收到",sentence):
            return None
    invoice_keyword = "|".join(["发票","报销凭证","专票"])
    
    invoice_xunwen = "正在为您查询，一会会以短信形式回复您发票开具情况"
    zhuanpiao_answer = "亲爱的，{}在{}资质通过的情况下正常的时效是订单完成后的[数字x]个工作日开具并寄出，[数字x]-[数字x]天会收到哦请您耐心等待下。"
    invoice_answer = "您好,咱们的电子发票是订单完成后[数字x]小时之内开具完成，下载方式:【端点击:我的—客户服务—我的发票—发票详情，电脑端:URL】"
    zhizhi_answer = "您好,下单时选择“普通发票（纸质）”自助开取，此发票可用作单位报销凭证，一个订单对应一张或多张发票，不同的物流中心发出的包裹开具不同的发票，发票会随每次包裹一同发出。"
    #发票关键词包括了  发票 电子发票 纸质发票  增值税发票 增税发票
    sign = "|".join(["(?=开)(?=票)","开.*凭证"])
    #if re.search(sign,sentence):
    if True:
        if re.search("显示运费",sentence):
            return "您好，若发票内容为明细，发票上会单独显示运费支付部分；若发票内容为非明细，发票上不会单独显示运费支付部分。"

        if re.search("余额支付",sentence):
            return "您好，余额支付金额部分是可以开具发票的。"
        
        if re.search("保修发票",sentence):
            return "您好，下单在提交订单页面可以选择发票类型，增值税专用发票电子发票售后保修三年的哦，出现质量问题,您是可以在您的订单里面提交售后返修申请的我们是有相关的售后工作人员审核的"
        
        if re.search("谁.*开",sentence):
            return "您好，一般情况下，京东自营的商品由京东提供发票；第三方卖家销售的商品由卖家开具并邮寄发票。"
        
        if re.search("维修商品",sentence):
            if re.search("返还",sentence):
                return "您好，换货和返修发票不和商品一起寄出，一般情况下，在您收到返修商品之后的一周左右为您寄出发票。"
        
        if re.search("金额",sentence):
            if re.search("不一致|不一样|不同|不对|不太对",sentence):
                return "您好，发票金额一般是您本次的实际支付金额。使用优惠券、京东卡/京东E卡、京豆等支付的金额不开发票。"
        
        if re.search("抬头",sentence):
            if not re.search("改",sentence):
                return "您好，发票抬头您可以选择个人或单位。"
        
        if re.search("多张发票",sentence):
            return "您好，一般情况下一张订单只能开具一张发票，但是订单购买多个商品，且发票开具内容为明细，一张发票无法全部开具的情况下，可能是会分开开具成一张以上的发票的。"        
        
        if re.search("嘛|么|吗|呢",sentence):
            if re.search("(没法|能|可以)报销",sentence):
                return "您好，电子发票是可以报销的"
        
        if re.search("没到|(没有|没)收到",sentence):    
            return "您好，您的发票预计[数字x]日送达到您手中."
               
        if re.search("可以.*[吗嘛么]|行[吗嘛么]",sentence):
            if re.search("增值税|专票|专用发票",sentence):return "您好只有等您的个人电子发票生成后才能修改为增值税专票哦"
            if re.search("个人.*公司|公司.*个人",sentence):return "可以的单位信息以及个人信息提供下"
            #if re.search("重新|修改",sentence):return "可以的，请问您有什么需要修改的信息么?"
            if re.search("(?=.*开)(?=.*票)",sentence):
                if not re.search("补开",sentence):return "亲爱的，可以的,在您下单前，可以在订单备注您需要的发票类型和抬头商家也是可以直接开具的呢"
            #return "亲爱的，可以的"
        
        if re.search("(开了|开出来了)(吗|嘛|么|没有)",sentence):
            return "您好，咱们的电子发票是订单完成后[数字x]小时之内开具完成，您可以通过电脑端:URL进行查询发票发票开具情况"

        if re.search("查",sentence):
            return "请您按照以下步骤【端我的客户服务发票下载使用】【电脑端我的京东客户服务我的发票发票详情下载使用】可在端打开URL进行发票查询和下载哦"
        if re.search("查询",sentence):
            return "亲，电子发票是需要订单完成后的[数字x]小时左右系统自动开具的，您这边在[数字x]小时左右查看一下即可，发票查询电脑端:我的订单—左侧的客户服务—我的发票—发票详情下载即可，下载链接URL;手机端:我的—客户服务—发票服务—查看发票哦，手机端链接://[链接x]"

        if re.search("时候",sentence):
            if re.search("到|寄",sentence):return "亲爱的，您开具的纸质发票会和商品一起邮寄过去的呢,专票的话则会单独邮寄，请您耐心等候"
            if re.search("补开",sentence):return "您好，补开时效是[数字x]天（以订单完成时间开始计算）。您可以使用【补开发票】自助功能，自行申请补开"
            return "亲爱的下单时选择普通发票电子自助订单完成后[数字x][数字x]天系统会自动开具可以点击我的客户服务发票发票详情下载"
                                            
        if re.search("催",sentence):
            return "嗯嗯，好的呢亲亲，这边帮您加急处理哈"
            
        if re.search("帮|要|怎样|怎么|如何|哪.*发票|哪里|开.*票",sentence):
            if re.search("设置.*信息",sentence):
                return "将商品加入购物车，点击去结算后，在“订单结算页”页面点击“发票信息”旁边的“修改”，可以修改发票类型（普通发票、增值税发票）、发票抬头（个人、公司），发票内容，发票抬头内容不能为空。"

            if re.search("补开发票",sentence):
                if re.search("图书",sentence):
                    return "您好，您下单时如忘记开具图书发票，京东自营图书商品可在180天内（以订单完成时间开始计算）可使用【补开发票】自助功能申请补开，或联系客服人员为您办理补开发票事宜，快递费用由京东承担。"
            

            if re.search("纸质发票",sentence):return "您好,下单时选择“普通发票（纸质）”自助开取，此发票可用作单位报销凭证，一个订单对应一张或多张发票，不同的物流中心发出的包裹开具不同的发票，发票会随每次包裹一同发出。"
            
            if re.search("电子发票",sentence):return "您好，下单时选择“普通发票（电子）”自助开取，订单完成后，系统会自动开具，用户可登陆京东个人账户，在订单详情页-付款信息页面下载。" 
            
            if re.search("增票|增值税发票|增税发票|专票|专用发票",sentence):
                if re.search("审核",sentence):return "我们会在[数字x]个工作日审核,审核通过后您下单选择对应的增票信息即可开具啦,#E-s[数字x]#E-s[数字x]#E-s[数字x],请问还有其他还可以帮到您的吗#E-s[数字x]"
                return "您好,下单时选择“增值税发票 ”自助开具。"
            
            if not re.search("[嘛吗]",sentence):
                return "您好，您在提交订单页面发票类型中选择好发票信息，有电子发票(增值税普通发票)、增值税专用发票供您选择"
        
#         if re.search("改|开错",sentence):
#             if re.search("(?=.*个人)(?=.*公司)",sentence):return "可以的单位信息提供下"
#             #if re.search("抬头",sentence):return "可以的，发票抬头提供下"
#             return "您好,您需要怎么修改发票?"

        if re.search("咨询",sentence):
            return "您好，请问有什么可以为您效劳#E-s[数字x]"
        
        
        if re.search("增票|增值税发票|增税发票|专票|专用发票|纸质|普通发票|电子发票",sentence):
            word = re.search("增值税发票|增税发票|专票|专用发票|纸质发票|普通发票|电子发票",sentence).group()
            if word =="电子发票":
                return "您好，您在提交订单页面发票类型中选择好发票信息，有电子发票(增值税普通发票)、增值税专用发票供您选择"#invoice_answer
            elif word in set(["纸质发票","普通发票"]):
                return zhizhi_answer
            elif word in set(["增值税发票","增税发票","专票","专用发票"]):
                if re.search("审核",sentence):return "我们会在[数字x]个工作日审核,审核通过后您下单选择对应的增票信息即可开具啦,#E-s[数字x]#E-s[数字x]#E-s[数字x],请问还有其他还可以帮到您的吗#E-s[数字x]"
                return zhuanpiao_answer.format(word,word)
            else:
                pass
#         else:
#             return "您好，您在提交订单页面发票类型中选择好发票信息，有电子发票(增值税普通发票)、增值税专用发票供您选择"
        
    return None


def invoiceReviseRule(sentence):
    '''
    dialogue stratege for invoice revise rule
    '''
    invoice_keyword = "|".join(["发票","报销凭证","专票"])
    content_keyword = '|'.join(['组织机构x', '数字x', 'ORDERID_DIGIT'])
    sign = '|'.join([ '改', '换',"重新","开错"])
    
    if re.search(sign, sentence):
        if re.search("时候|多久|多长时间",sentence):
            return "亲，[数字x]个工作日即可"
                
        if re.search("更换|换开|重新开",sentence):
            return "订单一旦生成无法更改，您可以提供下抬头和税号，等您的订单完成以后帮您换开#E-s[数字x]"
        
        if re.search("改|换",sentence):
            if re.search("组织机构x",sentence):
                return "这边帮您提交[组织机构x]的修改申请,请您耐心等待,待您的发票修改完成后我会短信告知您的"
            if re.search("姓名x",sentence):
                return "这边帮您提交的修改申请,请您耐心等待,待您的发票修改完成后我会短信告知您的"
            if re.search("发票类型",sentence):
                return "您好，等订单完成后，您可以申请换开发票类型"

        if re.search("发票.*改.*增.*票",sentence):
            return "亲爱的,您是想改成增值税发票是吗?为了更好的处理您的问题，我现在立刻为您升级至专员为您处理，我们的专员会在[数字x]小时之内联系您的，请您提供联系电话和姓名，谢谢"
            
        if re.search("(?=.*个人)(?=.*(公司|单位))|开公司",sentence):
            if re.search("[改换]为(公司|单位)",sentence):
                return "您好，请将您的单位信息提供下"
            if re.search("公司.*[改换].*个人",sentence):
                return "您好，如果您需要将抬头修改为公司，请将您的单位信息提供下；公司抬头无法改为个人抬头的"
            return "您好，请将您的单位信息提供下"
        
        if re.search('抬头|税号', sentence):
            return "亲亲亲请您提供一下要改的抬头和税号哦"
        
        if re.search("付款人",sentence):
            return "您好,这边核实到付款人是无法修改的呢"
        
        if re.search("可以.*[嘛么吗]",sentence):
            return "亲，您把公司抬头和税号发过来，我这边可以帮您记录修改呢"
            #return "亲，可以的呢，亲亲提供下您需要修改的内容哈#E-s[数字x]，电子发票需要修改的话要辛苦您提供一下您公司的开票信息哟谢谢"
        
        if re.search('想|给|帮|怎么|怎样|如何|(可以|能)修改[嘛吗么]', sentence):
            if re.search("打印",sentence):
                return "已提交申请修改好的发票[数字x]个工作日内开出，端:我的京东—客户服务—我的发票—发票详情下载即可;端:我的—客户服务—发票服务—发票详情查看即可;微信手端:京东优选—个人中心—订单详情查看即可载即可;"
            return "亲，您把公司抬头和税号发过来，我这边可以帮您记录修改呢" 
            #return "亲亲提供下您需要修改的内容哈#E-s[数字x]，电子发票需要修改的话要辛苦您提供一下您公司的开票信息哟谢谢"

        if re.search('公司|单位', sentence):
            #print("公司:{}".format(sentence))
            return "亲亲您提供一下需要修改的公司抬头和税号哦,【抬头:税号:您的手机联系方式:开明细还是大类】"
        
        if not re.search("不",sentence):
            return "亲，您把公司抬头和税号发过来，我这边可以帮您记录修改呢"
            #return "亲，你是要修改发票么，亲亲提供下您需要修改的内容哈#E-s[数字x]，电子发票需要修改的话要辛苦您提供一下您公司的开票信息哟谢谢"

    else:
        if re.search("组织机构x",sentence):
            return "这边帮您提交[组织机构x]的修改申请,请您耐心等待,待您的发票修改完成后我会短信告知您的"
        if re.search("姓名x",sentence):
            return "这边帮您提交的修改申请,请您耐心等待,待您的发票修改完成后我会短信告知您的"
#         if re.search("",sentence):
#             return 
    return None
