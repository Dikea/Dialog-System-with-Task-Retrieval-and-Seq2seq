#-*- coding: utf-8 -*- 


import sys
sys.path.append("..")
import codecs
import numpy as np
from search_dialog import config
from seq2seq_dialog.infer import get_infer_model, predict_sent_emb


model = get_infer_model("single_turn")

with codecs.open(config.context_response_path, "r", "utf-8") as rfd:
    corpus = rfd.read().splitlines()[:50000]
    corpus_len = len(corpus)
    sent_emb_index = np.zeros((corpus_len, 256), dtype=float)
    for idx, line in enumerate(corpus):
        if idx and idx % 1000 == 0:
            print ("idx=%d" % idx)
        context, response = line.strip().split("\t")
        sent_emb = predict_sent_emb(model, context) 
        sent_emb_index[idx, :] = sent_emb 
    print ("EmbShape: ", sent_emb_index.shape)
    np.save(config.sent_emb_index_path, sent_emb_index)
