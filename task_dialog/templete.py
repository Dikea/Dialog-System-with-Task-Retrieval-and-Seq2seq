#-*- coding: utf-8 -*-


import re


def intent_update(msg, dialog_status):
    dialog_status.intent = ""
    return dialog_status


def general_handle(msg, dialog_status):
    return None 
