#-*- coding: utf-8 -*-


import os


def file_path(dirname, file_name):
    module_path = os.path.dirname(__file__)
    file_path = os.path.join(module_path, dirname, file_name)
    return file_path


question_answer_path = file_path("data", "question_answer.txt")
context_response_path = file_path("data", "context_response.txt")
word2vec_path = "word2vec_model/v1.w2v_sgns_win2_d128.kv"
index_path = file_path("index", "similarity")
sent_emb_index_path = file_path("index", "sent_emb_index")
