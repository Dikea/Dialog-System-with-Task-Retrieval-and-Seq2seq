# -*- coding: utf-8 -*-

import sys
import codecs
from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.bleu_score import SmoothingFunction


def bleu(answerFilePath, standardAnswerFilePath):
    with codecs.open(answerFilePath, 'r', "utf-8") as rf_answer:
        with codecs.open(standardAnswerFilePath, 'r', "utf-8") as rf_standardAnswer:
            score = []
            answerLines = rf_answer.readlines()
            standardAnswerLines = rf_standardAnswer.readlines()
            chencherry = SmoothingFunction()
            for i in range(len(answerLines)):
                candidate = list(answerLines[i].strip())
                eachScore = 0
                for j in range(10):
                    reference = []
                    standardAnswerLine = standardAnswerLines[i*11+j].strip().split('\t')
                    reference.append(list(standardAnswerLine[0].strip()))
                    standardScore = standardAnswerLine[1]
                    bleuScore = sentence_bleu(reference,candidate,weights=(0.35,0.45,0.1,0.1),
                        smoothing_function=chencherry.method1)
                    eachScore = bleuScore * float(standardScore) + eachScore
                score.append(eachScore/10)
                eachScore = 0
            
            rf_answer.close()
            rf_standardAnswer.close()
            scoreFinal = sum(score)/float(len(answerLines))
            precisionScore = round(scoreFinal,6)
            return precisionScore                   


if __name__ == "__main__":
    candidateFilePath = sys.argv[1]
    referenceFilePath = sys.argv[2]
    score_final = bleu(candidateFilePath,referenceFilePath)
    print(score_final)               
