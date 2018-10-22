#-*- coding: utf-8 -*-


import re
from task_dialog import start_task
from task_dialog import unbind_task 
from task_dialog import price_protect_task
from task_dialog import invoice_task
from task_dialog import sale_task
from task_dialog import refund_task
from task_dialog import sale_after_task
from task_dialog import query_task
from task_dialog import order_modify
from task_dialog import order_related_task
from task_dialog import delivery_task
from task_dialog import general_task
from task_dialog import short_query_task
from task_dialog import finish_task
from utils.tools import log_print


class TaskCore(object):


    intent_update_func = [
        ("start", "start_task.intent_update"),
        ("unbind", "unbind_task.intent_update"),
        ("price_protect", "price_protect_task.intent_update"),
        ("invoice", "invoice_task.intent_update"),
        ("sale_return", "sale_task.intent_update"),
        ("sale_after", "sale_after_task.intent_update"),
        ("refund", "refund_task.intent_update"),
        ("order_modify", "order_modify.intent_update"),
        ("query", "query_task.intent_update"),
        ("order_related", "order_related_task.intent_update"),
        ("delivery", "delivery_task.intent_update"),
        ("general", "general_task.intent_update"),
        ("finish", "finish_task.intent_update"),
        ("short_query", "short_query_task.intent_update"),
    ]

    intent_not_reset = set(["sale_return", "refund", "invoice", "unbind", "price_protect"])
    
    intent_handle_func = {
        "start": "start_task.start_handle", # 用户对话开启
        "unbind": "unbind_task.unbind_handle", # 解绑相关
        "price_protect": "price_protect_task.price_protect_handle", # 价格保护
        "invoice": "invoice_task.invoice_handle", # 发票 
        "sale_return": "sale_task.sale_return", # 退货
        "sale_after": "sale_after_task.sale_after", # 换货
        "refund": "refund_task.refund_response", # 退款
        "order_modify": "order_modify.order_modify_handle", # 订单修改
        "query": "query_task.query_judge", # 查询询问
        "order_related":"order_related_task.order_related",# 客服订单相关回复
        "delivery":"delivery_task.delivery", # 客服物流快递配送相关回复
        "general": "general_task.general_handle", # 常见问题回复 
        "finish":"finish_task.finish_handle", # 用户对话结束
        "short_query": "short_query_task.short_query_handle", # 短query处理
    }


    @classmethod
    def _slots_update(cls, msg, dialog_status):
        if re.search("\[ORDER.*\]", msg):
            dialog_status.order_id = re.search("\[ORDER.*\]",msg).group()
            return dialog_status
        if len(dialog_status.context)>1:
            his_response = dialog_status.context[-2]
            if re.search("提供.*订单号",his_response):
                if re.search("\[数字x\]",msg):
                    dialog_status.order_id = "[ORDERID_[数字x]]"
        return dialog_status

    
    @classmethod
    def task_handle(cls, msg, dialog_status):
        try:
            response = None

            if dialog_status.intent not in cls.intent_not_reset:
                dialog_status.intent = None
                
            for intent, update_func in cls.intent_update_func:
                dialog_status = cls._slots_update(msg, dialog_status)
                dialog_status = eval(update_func)(msg, dialog_status)
                if dialog_status.intent == intent:
                    handle_func = cls.intent_handle_func[dialog_status.intent]
                    response = eval(handle_func)(msg, dialog_status)
                    if response:
                        break

            log_print("intent=%s, task_response=%s" % (dialog_status.intent, response))
            return response, dialog_status
        except Exception as e:
            log_print("[ERROR] msg=%s, errmsg=%s" % (msg, e))
            return response, dialog_status
