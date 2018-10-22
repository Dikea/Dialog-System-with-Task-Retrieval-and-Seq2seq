#-*- coding: utf-8 -*-


import search_dialog
from search_dialog.tfidf_model import TfidfModel
from search_dialog.bm25_model import BM25Model
from seq2seq_dialog.data_helpers import loadDataset
from utils.tools import log_print


SEARCH_MODEL = "bm25"


class SearchCore(object):

    word2id, _ = loadDataset(vocab_size=10000) 
    if SEARCH_MODEL == "tfidf":
        qa_search_inst = TfidfModel(search_dialog.config.question_answer_path, 
            scale="large", word2id=word2id) 
        cr_search_inst = TfidfModel(search_dialog.config.context_response_path,
            scale="large", word2id=word2id)
    elif SEARCH_MODEL == "bm25":
        qa_search_inst = BM25Model(search_dialog.config.question_answer_path, 
            word2id=word2id)
        cr_search_inst = BM25Model(search_dialog.config.context_response_path,
            word2id=word2id)


    @classmethod
    def search(cls, msg_tokens, mode="qa", filter_pattern=None):
        query = [w for w in msg_tokens if w in cls.word2id]
        search_inst = cls.qa_search_inst if mode == "qa" else cls.cr_search_inst
        sim_items = search_inst.similarity(query, size=10)
        docs, answers = search_inst.get_docs(sim_items)

        # User filter pattern.
        if filter_pattern:
            new_docs, new_answers = [], []
            for doc, ans in zip(docs, answers):
                if not filter_pattern.search(ans):
                    new_docs.append(doc)
                    new_answers.append(ans)
            docs, answers = new_docs, new_answers

        log_print("init_query=%s, filter_query=%s" % ("".join(msg_tokens), "".join(query)))
        response, score = answers[0], sim_items[0][1] 
        log_print("%s_search_sim_doc=%s, score=%.4f" % (mode, "".join(docs[0]), score))
        if score <= 1.0:
            response, score = "亲爱哒，还有什么小妹可以帮您呢~", 2.0
        return response, score
