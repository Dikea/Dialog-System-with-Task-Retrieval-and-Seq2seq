#-*- coding: utf-8 -*-


import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"


def file_path(dirname, file_name):
    module_path = os.path.dirname(__file__)
    file_path = os.path.join(module_path, dirname, file_name)
    return file_path


vocab_path = file_path("data", "vocab.txt")
single_train_path = file_path("data", "single_train.txt")
multi_train_path = file_path("data", "multi_train.txt")
version = "v0"
model_path = file_path("model", version)

"""
# Evaluate
single_questions_path = file_path("test_data", "single_questions.txt")
single_answers_path = file_path("test_data", "single_answers.txt")
multi_questions_path = file_path("test_data", "multi_questions.txt")
multi_answers_path = file_path("test_data", "multi_answers.txt")
"""

word2vec_path = file_path("model", "word2vec.model")
embeddings_path = file_path("model", "word.embeddings")


class Params(object):
    rnn_size = 256 
    num_layers = 1
    embedding_size = 300
    vocab_size = 10000
    learning_rate = 0.001
    batch_size = 80
    numEpochs = 15
    steps_per_checkpoint = 300
    model_name = "chatbot.ckpt"
    beam_size = 10
    max_gradient_norm = 5.0
    use_attention = True
    bidirectional_rnn = False
