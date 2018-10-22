#!/usr/bin/python3
#-*- coding: utf-8 -*-


from search_dialog.search_core import SearchCore
from seq2seq_dialog.infer import get_infer_model, predict 
from task_dialog.task_core import TaskCore
from utils.nlp_util import NlpUtil
from utils.tools import ch_count
from utils.tools import log_print


class DialogStatus(object):

    def __init__(self):
        self.intent = None

        # Universal slots
        self.ware_id = None
        self.order_id = None

        # Special slots
        self.start_flag = None
        self.sale_return_intent = None
        self.invoice_intent = None
        self.query_intent = None
        self.order_related = None

        # unbind
        self.unbind_flag = None
        self.unbind_identify = None
        self.unbind_phone = None
        self.unbind_new_phone = None
        self.unbind_success = None

        # price protect
        self.price_protect_success = None
     
        # dialog context
        self.context = []


class DialogManagement(object):

    seq2seq_inst = get_infer_model(dialog_mode="multi_turn")
    dialog_status = DialogStatus()


    @classmethod
    def _predict_via_seq2seq(cls, msg_tokens):
        user_msgs = " ".join(cls.dialog_status.context[::2][-4:])
        log_print("seq2seq_input=%s" % user_msgs)
        response = predict(cls.seq2seq_inst, user_msgs, ret_size=1)
        return response


    @classmethod
    def process_dialog(cls, msg, use_task=True):
        """
        Dialog strategy: use sub-task to handle dialog firstly,
        if failed, use retrieval or generational func to handle it.
        """
        # Task response.
        if use_task:
            task_response, cls.dialog_status = TaskCore.task_handle(
               msg, cls.dialog_status)
        else:
            task_response = None

        # Search response.
        if len(cls.dialog_status.context) >= 3 and ch_count(msg) <= 4:  
            user_msgs = cls.dialog_status.context[::2][-3:]
            msg = "<s>".join(user_msgs)
            mode = "cr"
        else:
            mode = "qa"
        msg_tokens = NlpUtil.tokenize(msg, True)
        search_response, sim_score = SearchCore.search(msg_tokens, mode=mode)
        
        # Seq2seq response.
        seq2seq_response = cls._predict_via_seq2seq(msg_tokens)
        log_print("search_response=%s" % search_response)
        log_print("seq2seq_response=%s" % seq2seq_response)

        if task_response:
            response = task_response
        elif sim_score >= 1.0:
            response = search_response
        else:
            response = seq2seq_response

        return response

        
def start_dialog():

    print ("\nChatbot: %s\n" % ("您好，我是可爱的人工智能机器人小智，有问题都可以向我提问哦~"))
    print ("input1: ", end="")

    while True:
        msg = input().strip()
        if msg.lower() == "finish":
            DialogManagement.dialog_status = DialogStatus()
            print ("Chatbot: %s\n\n" % "change session", end="")
            print ("input1: ", end="")
        elif msg.lower() == "exit":
            print ("Chatbot: %s\n\n" % ("感谢您对京东的支持，我们下次再见呢~, 拜拜亲爱哒"))
            exit() 
        else:
            DialogManagement.dialog_status.context.append(msg)
            response = DialogManagement.process_dialog(msg, use_task=True)
            DialogManagement.dialog_status.context.append(response)
            print ("output%d: %s\n\n" % (len(DialogManagement.dialog_status.context) / 2, response), end="")
            print ("input%d: " % (len(DialogManagement.dialog_status.context) / 2 + 1), end="")
            

if __name__ == "__main__":
    start_dialog()
