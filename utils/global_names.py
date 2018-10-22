#-*- coding: utf-8 -*-


import os


class GlobalNames(object):


    # Tokenize config file
    PUNCTUATIONS_FILE = "punctuations.txt"
    STOPWORDS_FILE = "stopwords.txt"
    USER_DEFINE_WORDS = "user_define_words.txt" 
    REMOVE_WORDS_FILE = "remove_words.txt"
    ORDER_INFO_FILE = "order.txt"

    # Tfidf config file
    CORPUS_DICT_FILE = "corpus.dict"
    CORPUS_TFIDF_FILE = "corpus.tfidf_model"

    # ES config
    ELASTICSEARCH_CFG = {
        "hosts": "localhost:9200",
        "timeout": 30,
        "doc_index": "dialog_v0",
        "doc_type": "post_response",
    }


def get_file_path(file_name):
    module_path = os.path.dirname(__file__)
    file_path = os.path.join(module_path, 'conf', file_name)
    return file_path
