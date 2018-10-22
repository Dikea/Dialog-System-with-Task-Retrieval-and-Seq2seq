#-*- coding: utf-8 -*-


import codecs
from gensim import corpora
from gensim.models import LdaModel
from gensim.corpora import Dictionary


train_size = 10000
input_file = "../seq2seq_dialog/data/single_train.txt"


with codecs.open(input_file, "r", "utf-8") as rfd:
    data = rfd.read().splitlines()[:train_size]
    raw_corpus = [s.split("\t")[0] for s in data]
    raw_corpus = [s.split() for s in raw_corpus]
 
dictionary = corpora.Dictionary(raw_corpus)
corpus = [ dictionary.doc2bow(text) for text in raw_corpus]
lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=100)
 
topic_list=lda.print_topics(20)
 
for topic in topic_list:
    print (topic)
