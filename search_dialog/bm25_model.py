#-*- coding: utf-8 -*-


import time
import codecs
from utils.bm25_util import BM25Util
from gensim.summarization import bm25


DEBUG_MODE = True


class BM25Model(object):

    def __init__(self, corpus_file, word2id):
        time_s = time.time()
        size = 500000 if DEBUG_MODE else 10000000
        with codecs.open(corpus_file, "r", "utf-8") as rfd:
            data = [s.strip().split("\t") for s in rfd.readlines()[:size]]
            self.contexts = [[w for w in s.split() if w in word2id] for s, _ in data]
            self.responses = [s.replace(" ", "") for _, s in data]
        self.bm25_inst = BM25Util(self.contexts) 
        print ("Time to build bm25 model: %2.f seconds." % (time.time() - time_s))


    def similarity(self, query, size=10):
        return self.bm25_inst.similarity(query, 10) 


    def get_docs(self, sim_items):
        docs = [self.contexts[id_] for id_, score in sim_items]
        answers = [self.responses[id_] for id_, score in sim_items]
        return docs, answers
