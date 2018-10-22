import re


def intent_update(msg,dialog_status):
    sign = "|".join(["商品","售后","换货","货物","东西"])
    if re.search(sign,msg):
        dialog_status.intent = "sale_after"
    elif dialog_status.intent == "sale_after":
        dialog_status.intent = None
    
    return dialog_status


def sale_after(sentence,dialog_status):
    
    if re.search("商品|货物|东西",sentence):
        
        if re.search("质量问题|有问题",sentence):
            return "您好，商品有质量问题京东支持7天退货、15天内换货、质保期内保修。"
        
        if re.search("保修时间",sentence):
            return "您好，商品保修时间以您收货时间开始计算。"
        
        if re.search("买错了",sentence):
            return "您好，您购买的商品都是经过细心挑选的，若不影响您的正常使用，建议您可以正常继续使用；若影响您的正常使用，您可以在售后申请时效内尽快提交售后申请，会有专业的工作人员为您审核处理。"
        
        if re.search("预售",sentence):
            return "您好，预售商品的售后政策和正常商品售后政策相同。"
        
    if re.search("售后",sentence):
        if re.search("审核",sentence):
            if re.search("没有通过|未通过",sentence):
                return "您好，您可以登陆京东首页>我的京东>左侧客户服务>返修/退换货>查看返修/退换货记录，在相应服务单号后点击“查看”即可。"
            return "请您在电脑端登录京东商城账户，在我的京东-返修退换货，查看相应返修/退换货记录"
        
        
    if re.search("换货",sentence):
        if re.search("多长时间|多久",sentence):return "您好，换货处理自接收到问题商品之日起7日之内处理完成"

        if re.search("地址",sentence):return "服务单审核完毕后，系统会自动发短信通知您返回地址。"
        
        if re.search("进度",sentence):return "您好，您可以点击我的>退换/售后>进度查询，找到对应的退换货商品，点击右上角“进度查询”，即可查看服务单进度。"
        
        if re.search("到付",sentence):return "不可以使用到付的呢，亲"
        
        if re.search("运费|邮费|快递费",sentence):return "您好，因非商品质量问题由客户发起的换货行为，将由客户承担返回京东的运费。"
        
        return "您好，目前针对换货，只支持换同个商品编号的同款商品，暂不支持更换其它商品。"
    
    
    return None
    