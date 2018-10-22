#-*- coding: utf-8 -*-


import re
from search_dialog.search_core import SearchCore
from utils.nlp_util import NlpUtil


info_supply_pattern = re.compile(r"(?=.*提供)(?=.*(姓名|号码|手机号|联系方式))") 


def intent_update(msg, dialog_status):
    if len(dialog_status.context) >= 3:
        last_response = dialog_status.context[-2]
        if info_supply_pattern.search(last_response):
            dialog_status.intent = "info_supply"
    return dialog_status


def info_supply_handle(msg, dialog_status):
    last_msg = dialog_status.context[-3]
    msg_tokens = NlpUtil.tokenize(last_msg, True)
    response, _ = SearchCore.search(msg_tokens, info_supply_pattern)
    return response
