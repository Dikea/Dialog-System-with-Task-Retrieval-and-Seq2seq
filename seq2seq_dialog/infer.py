#-*- coding: utf-8 -*-


import os
import numpy as np
import tensorflow as tf
from seq2seq_dialog.data_helpers import loadDataset, getBatches, sentence2enco
from seq2seq_dialog.model import Seq2SeqModel
from seq2seq_dialog import config


word2id, id2word = loadDataset(vocab_size=config.Params.vocab_size)
Params = config.Params
Params.beam_search = True


def get_infer_model(dialog_mode):
    tf.reset_default_graph()
    sess = tf.Session()
    model_path = os.path.join(config.model_path, dialog_mode)
    with tf.variable_scope("Model"):
        model = Seq2SeqModel(sess, "decode", Params, word2id)
    ckpt = tf.train.get_checkpoint_state(model_path)
    model.saver.restore(model.sess, ckpt.model_checkpoint_path)
    print ("Load seq2seq model from %s done." % model_path)
    return model


def _predict_ids_to_seq(predict_ids, id2word, beam_size):
    predicts = []
    for single_predict in predict_ids:
        for i in range(beam_size):
            predict_list = np.ndarray.tolist(single_predict[:, :, i])
            predict_seq = [id2word[idx] for idx in predict_list[0] 
                if idx in id2word if idx >=4]
            predicts.append("".join(predict_seq))
    return predicts


def predict(model, context, ret_size=5):
    batch = sentence2enco(context, word2id)
    predicted_ids = model.infer(batch)
    result = _predict_ids_to_seq(predicted_ids, id2word, beam_size=5)
    return result[0]


def predict_sent_emb(model, context):
    batch = sentence2enco(context, word2id)
    sent_emb = model.infer_sent_emb(batch)[0]
    return sent_emb
