#-*- coding: utf-8 -*-


import sys
sys.path.append("..")
import codecs
import numpy as np
from utils.nlp_util import NlpUtil
from search_dialog import config
from seq2seq_dialog.infer import get_infer_model, predict_sent_emb


class SentEmbSearch(object):

    
    sent_emb_index = np.load(config.sent_emb_index_path + ".npy")
    id2info = {}
    with codecs.open(config.context_response_path, "r", "utf-8") as rfd:
        cnt = 0
        for line in rfd:
            context, response = line.strip().split("\t")
            id2info[cnt] = [context.replace(" ", ""), response.replace(" ", "")]
            cnt += 1
        print ("Load corpus done, corpus_size=%d" % cnt)


    @classmethod 
    def search(cls, model, sent, size=10):
        sent_emb = predict_sent_emb(model, sent) 
        sims = np.dot(cls.sent_emb_index, sent_emb.T)
        print (sims)
        sim_items = [(idx, sim_score) for idx, sim_score in enumerate(sims)]
        sim_items.sort(key=lambda x: x[1], reverse=True)
        sim_items = sim_items[:size]
        print (sim_items)
        contexts = [cls.id2info[idx][0] for idx, _ in sim_items]
        responses = [cls.id2info[idx][1] for idx, _ in sim_items]
        return sim_items, contexts, responses
        

if __name__ == "__main__":
    model = get_infer_model("single_turn")
    q = "分期购买机子回去 用了一段时间不适合有任何问题可以申请退货退款吗"
    _, cs, rs = SentEmbSearch.search(model, "分期购买机子回去 用了一段时间不适合有任何问题可以申请退货退款吗")
    for c, r in zip(cs, rs):
        print (c)
        print (r)
        print ()


