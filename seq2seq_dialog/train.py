# -*- coding: utf-8 -*-


import os
import sys
sys.path.append("../")

import math
import time
import codecs
import numpy as np
import tensorflow as tf
from seq2seq_dialog.data_helpers import loadDataset, getBatches
from seq2seq_dialog.data_helpers import sentence2enco
from seq2seq_dialog.model import Seq2SeqModel
from seq2seq_dialog.evaluate import evaluate
from seq2seq_dialog import config


tf.app.flags.DEFINE_string("dialog_mode", "single_turn", "single turn or multi turn")
FLAGS = tf.app.flags.FLAGS
Params = config.Params

if not os.path.exists(config.model_path):
    os.mkdir(config.model_path)
model_dir = os.path.join(config.model_path, FLAGS.dialog_mode) 
checkpoint_path = os.path.join(model_dir, Params.model_name)

if FLAGS.dialog_mode == "single_turn":
    train_path = config.single_train_path
else:
    train_path = config.multi_train_path
word2id, id2word, trainingSamples = loadDataset(train_path, vocab_size=Params.vocab_size)

log_f = codecs.open("log/%s.%s.log" % (FLAGS.dialog_mode, config.version), "w", "utf-8")
for name, value in vars(Params).items():
    log_f.write("%s\t%s\n" % (name, value))


def log_print(text):
    print(text)
    log_f.write(text + "\n")
   

def train_model():
    sess = tf.Session() 
    log_print("Dialog_mode: %s" % FLAGS.dialog_mode)
    # Define train/eval model.
    with tf.name_scope("Train"):
        with tf.variable_scope("Model", reuse=None):
            Params.beam_search = False
            train_model = Seq2SeqModel(sess, "train", Params, word2id)
        ckpt = tf.train.get_checkpoint_state(model_dir)
        if ckpt and tf.train.checkpoint_exists(ckpt.model_checkpoint_path):
            log_print('Reloading model parameters..')
            train_model.saver.restore(sess, ckpt.model_checkpoint_path)
        else:
            log_print('Created new model parameters..')
            sess.run(tf.global_variables_initializer())

    with tf.name_scope("Eval"):
        with tf.variable_scope("Model", reuse=True):
            Params.beam_search = True
            eval_model = Seq2SeqModel(sess, "decode", Params, word2id)

    current_step = 0
    best_score = 0.0
    for epoch in range(Params.numEpochs):
        time_s = time.time()
        log_print("\nEpoch %d/%d" % (epoch + 1, Params.numEpochs))
        batches = getBatches(trainingSamples, Params.batch_size)
        for nextBatch in batches:
            loss, summary = train_model.train(nextBatch)
            current_step += 1
            if current_step % Params.steps_per_checkpoint == 0:
                perplexity = math.exp(float(loss)) if loss < 300 else float('inf')
                log_print("step=%d, loss=%.2f, perplexity=%.2f" % (current_step, loss, perplexity))
                train_model.saver.save(train_model.sess, checkpoint_path)
                """
                bleu_score = evaluate(eval_model, FLAGS.dialog_mode) 
                if bleu_score >= best_score:
                    best_score = bleu_score
                    train_model.saver.save(train_model.sess, checkpoint_path)
                    log_print("BleuScore improved, score=%.4f, save model" % (bleu_score))
                else:
                    log_print("BleuScore reduced, score=%.4f" % (bleu_score))
                """
        time_e = time.time()
        log_print ("Epoch %d training done, time=%.2f minutes" % (epoch + 1, (time_e - time_s) / 60))


if __name__ == "__main__":
    train_model()
