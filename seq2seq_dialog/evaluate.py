#-*- coding: utf-8 -*-


import codecs
from seq2seq_dialog.infer import predict
from seq2seq_dialog import config
from scripts.bleu import bleu


record_length = 6


def _process_gen_msg(text):
    text = text.replace("URL", "http")
    return text


def single_dialog(model, context):
    answer = predict(model, context, ret_size=1)
    answer = _process_gen_msg(answer)
    return answer


def multi_dialog(model, questions):
    results = []
    q_len = len(questions)
    for idx in range(q_len):
        #context = "<s>".join(questions[max(0, idx + 1 - record_length): idx + 1])
        context = questions[-1]
        answer = predict(model, context, ret_size=1)
        answer = _process_gen_msg(answer)
        results.append(answer)
    return results


def evaluate(model, dialog_mode):
    result_path = "log/%s.%s.result" % (dialog_mode, config.version)
    if dialog_mode == "single_turn":
        with codecs.open(config.single_questions_path, "r", "utf-8") as rfd, \
            codecs.open(result_path, "w", "utf-8") as wfd:
            for line in rfd:
                line = line.strip("\r\n")
                answer = single_dialog(model, line)
                wfd.write("%s\n" % answer)  
        return bleu(result_path, config.single_answers_path)
    else:
        with codecs.open(config.multi_questions_path, "r", "utf-8") as rfd, \
            codecs.open(result_path, "w", "utf-8") as wfd:
            questions = []
            for line in rfd:
                line = line.strip("\r\n")
                if line != "":
                    questions.append(line)
                else:
                    answers = multi_dialog(model, questions)
                    for answer in answers:
                        wfd.write("%s\n" % answer)
                    questions = []
            answers = multi_dialog(model, questions)
            for answer in answers:
                wfd.write("%s\n" % answer)
        return bleu(result_path, config.multi_answers_path)
