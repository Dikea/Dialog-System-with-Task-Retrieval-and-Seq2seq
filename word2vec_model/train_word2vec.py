#-*- encoding: utf-8 -*-


import sys
import codecs
from gensim import models


def _input_streaming(in_fpath, return_raw = False):
    with codecs.open(in_fpath, "r", "utf-8") as rfd:
        for line in rfd:
            word_seg = line.strip("\n").split()
            yield word_seg


def train_word2vec_model(corpus_fpath, wv_fpath = None):
    vec_size = 300
    win_size = 2
    with codecs.open(corpus_fpath, "r", "utf-8") as rfd:
        corpus_ = rfd.readlines()
        corpus_ = [s.split() for s in corpus_]
    # begin to train
    print("begin to train model...")
    w2v_model = models.word2vec.Word2Vec(corpus_,
                                         size = vec_size,
                                         window = win_size,
                                         min_count = 2,
                                         workers = 4,
                                         sg = 1,
                                         negative = 15,
                                         iter = 7)
    w2v_model.train(_input_streaming(corpus_fpath), 
        total_examples=len(corpus_), epochs=w2v_model.iter)
    if wv_fpath:
        wv = w2v_model.wv
        fname = "%s.w2v_sgns_win%s_d%s.kv" % (wv_fpath, win_size, vec_size)
        wv.save_word2vec_format(fname) 
    print("save model success, model_path=%s" % (fname))


def load_word_vector(w2v_fpath):
    wv = models.KeyedVectors.load_word2vec_format(w2v_fpath, binary = False)
    return wv


if "__main__" == __name__:
    corpus_fpath = sys.argv[1] 
    wv_fpath = "./word2vec_model/v1"
    train_word2vec_model(corpus_fpath, wv_fpath)
