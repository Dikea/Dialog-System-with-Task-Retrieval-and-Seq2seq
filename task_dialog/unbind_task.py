#-*- coding: utf-8 -*-


import re


unbind_pattern = re.compile(r"解绑|换.*绑|(?=.*(换|改|更|绑定))(?=.*(手机|电话))")


def intent_update(msg, dialog_status):
    if unbind_pattern.search(msg):
        dialog_status.intent = "unbind"
        if re.search(r"手机|电话", msg):
            dialog_status.unbind_phone = True
    return dialog_status


def unbind_handle(msg, dialog_status):
    if not dialog_status.unbind_flag:
        dialog_status.unbind_flag = True
        return ("[数字x]，为了更好的处理您的账户问题，需要跟您核对[数字x]项左右信息，保证账户安全，"
            "尽快为您换绑或者解绑，绑定，麻烦您提供一下该账号之前订单常用收货人姓名，收货地址以及收"
            "货手机号码呢，如果忘记了，需要您提供下身份证号码和姓名呢")
    elif dialog_status.unbind_phone and not dialog_status.unbind_new_phone:
        dialog_status.unbind_new_phone = True
        return ("亲爱的，现在需要绑定的手机号是什么呢?")
    elif not dialog_status.unbind_identify:
        dialog_status.unbind_identify = True 
        return ("您好，这边给您手机发送了一条验证码，还请您提供一下，麻烦了呢")
    elif not dialog_status.unbind_success:
        dialog_status.unbind_success = True
        return ("亲爱的，已经为您的账户换绑成功哦#E-s[数字x]")
    return None 
