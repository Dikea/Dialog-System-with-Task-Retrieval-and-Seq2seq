#-*- coding: utf-8 -*-


from gensim import models
from gensim.similarities import WmdSimilarity


class WmdUtil(object):

    def __init__(self, word2vec_path):
        self.word2vec = models.KeyedVectors.load_word2vec_format(
            word2vec_path, binary=False)
        self.word2vec.init_sims(replace=True)
        print ("Load word2bec model done.")


    def similarity(self, query, docs, size=10):
        wmd_inst = WmdSimilarity(docs, self.word2vec, 
            num_best=size, normalize_w2v_and_replace=False)
        sims = wmd_inst[query]
        return sims
