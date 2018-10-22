#-*- coding: utf-8 -*-


import re

def intent_update(msg,dialog_status):
    sign = "订单|下单|下的单"
    if re.search(sign,msg):
        dialog_status.order_related = True
        dialog_status.intent = "order_related"
    else:
        dialog_status.order_related = False
        if dialog_status.intent == "order_related":
            dialog_status.intent = None
    return dialog_status


def order_related(sentence,dialog_status):
    sign = "订单|下单|下的单"
#     if re.search(sign,sentence):
    if True:
        if re.search("取消",sentence):
            if re.search("注意事项",sentence):
                return "1订单若包含赠品、加购价、满减等促销商品，若主商品订单取消，关联促销商品也将取消;2已收货的订单，请申请返修\退换;3提交订单取消申请后，系统会帮您拦截订单，并为您办理退款，如果订单取消失败，您可根据需要签收或者拒收" 
            if re.search("优惠券",sentence):
                return "使用全品类东券、限品类东券、店铺东券、平台专享类东券提交的订单，若订单未拆分，则订单取消后，系统自动返还相应的东券；若订单被拆分，取消全部子单，系统自动返还相应的东券；"
            if re.search("帮|如何|怎么",sentence):
                return  "登陆京东app客户端，点击页面右下方【我的】-【我的订单】,点击进入需要取消的订单，点击右下角【取消订单】"
            if re.search("恢复",sentence):
                return "您好，订单一旦取消，将无法恢复，请您慎重操作"
            if re.search("预售",sentence):
                return "您好，预售订单不可以取消，预售活动结束后，若未支付尾款，订单自动取消，取消后定金不退。"
            
        if re.search("改送",sentence):
            return "京东发货的订单，在订单打印前，可以修改末级收货地址，打开订单详情页面，点击右上角修改按钮即可，如无修改按钮，则说明订单已经无法进行修改。"
        if re.search("取货",sentence):
            return "您好，部分站点支持自提货物，自取前请与配送或站点先行联系确认。"
        
        if re.search("送达",sentence):
            return "在商品现货的情况下，自营商品，北京、上海、广州的客户下单后一般24小时内可收到货.其它地区用户,一般到货时间在1-7天."
        
        if re.search("返回调度",sentence):
            return "您好,由于系统原因，商品有时会分拣到错误站点，需要返回调度中心重新分拣安排配送，因此给您带来的不便我们表示万分抱歉，请您耐心等待，后续注意查收即可。"
        
        if re.search("退款",sentence):
            if re.search("多久|什么时候|什么时间",sentence):
                return "京东商品订单拒收后，在线支付订单您可以在前台提交退款申请，也可以联系客服为您提交退款申请，待商品返回，我司为您审核退款，退款审核成功后，具体退款周期还请您查看：URL如您的订单退款超过退款周期仍未收到退款，请您联系客服进行处理。"
            if re.search("怎么",sentence):
                return "您好，在线支付的订单取消成功后，我们会给您提供'订单快速退款'服务."
            
        if re.search("多久|什么时候|什么时间",sentence):
            if re.search("发货",sentence):
                return "请您耐心等候，商品到货，我们会尽快给您安排发货"
            if re.search("到",sentence):
                return "在商品现货的情况下，自营商品，北京、上海、广州的客户下单后一般24小时内可收到货.其它地区用户,一般到货时间在1-7天."
            
        if re.search("第三方",sentence):
            if re.search("卖家驳回|卖家拒绝",sentence):
                return "若订单还未发出，请联系京东在线客服再次申请取消订单，或申请交易纠纷。"

        if re.search("查看|进度|查询|订单情况|什么状态|什么情况|订单状态",sentence):
            return "在京东首页点击右上角【我的订单】即可查询到下单记录。"
        
        if re.search("多付|付多|多支付|支付少",sentence):
            return "您好，多付款的订单，在订单完成之后，系统会自动把多支付的款项退还给您。"
        
        if re.search("少付|付少|少支付|支付少",sentence):
            return "您好，请刷新页面，重新点击“支付”按钮支付剩余金额即可。"
        
       
    return None
