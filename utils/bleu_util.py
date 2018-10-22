#-*- coding: utf-8 -*-


from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.bleu_score import SmoothingFunction


chencherry = SmoothingFunction()


def bleu_score(candidate, reference):
    score = sentence_bleu(
        [list(reference)], list(candidate),
        weights=(0.25, 0.25, 0.25, 0.25),
        smoothing_function=chencherry.method1)
    return score


def bleu_similarity(query, docs):
    scores = [(idx, bleu_score(doc, query))
        for idx, doc in enumerate(docs)]
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores
