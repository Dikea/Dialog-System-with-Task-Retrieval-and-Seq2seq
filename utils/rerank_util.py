#-*- coding: utf-8 -*-


from collections import defaultdict
from scipy.stats import rankdata
from utils.wmd_util import WmdUtil
from utils.nlp_util import NlpUtil
from utils.bm25_util import BM25Util
from utils.bleu_util import bleu_similarity
from search_dialog import config 


wmd_inst = WmdUtil(config.word2vec_path)


def _normalize_feature(feature):
    scores = [score for _, score in feature]
    rank = rankdata(scores) / len(scores)
    normalized_feature = [(item[0], rank_digit)
        for rank_digit, item in zip(rank, feature)]
    return normalized_feature


def bagging(features, weights, normalize=True):
    if normalize:
        features = [_normalize_feature(feature) for feature in features]
    print (features)
    final_scores = defaultdict(float)
    weight_sum = sum(weights)
    for feature, weight in zip(features, weights):
        for idx, score in feature:
            final_scores[idx] += score * weight
    for idx in final_scores.keys():
        final_scores[idx] /= weight_sum
    final_scores = list(final_scores.items())
    final_scores.sort(key=lambda x: x[1], reverse=True)
    print (final_scores)
    return final_scores


def rerank(tfidf_feature, query, docs):
    # Build features
    for idx, item in enumerate(tfidf_feature):  
        tfidf_feature[idx] = (idx, item[1])
    bm25_inst = BM25Util(docs)
    bm25_feature = bm25_inst.similarity(query) 
    wmd_feature = wmd_inst.similarity(query, docs)

    # Bagging features
    if wmd_feature:
        features = [tfidf_feature, wmd_feature]
        weights = [0.5, 0.5]
    else:
        features = [tfidf_feature]
        weights = [1.0]
    final_scores = bagging(features, weights, normalize=False)
    index, score = final_scores[0]

    return index, score 
