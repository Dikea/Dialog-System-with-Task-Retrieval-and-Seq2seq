#!/usr/bin/python3
#-*- coding: utf-8 -*-


import os
import re
import copy
import jieba
import codecs
import jieba.analyse
import jieba.posseg as pseg
from gensim import corpora
from gensim import models
from utils.global_names import GlobalNames, get_file_path 


def _load_words(file_name):
    file_path = get_file_path(file_name)
    with codecs.open(file_path, "r", "utf-8") as rfd:
        words_set = set(rfd.read().splitlines())
    return words_set


class NlpUtil(object):

    punctuations_set = _load_words(GlobalNames.PUNCTUATIONS_FILE)
    stopwords_set = _load_words(GlobalNames.STOPWORDS_FILE)
    user_define_words = _load_words(GlobalNames.USER_DEFINE_WORDS)
    remove_words_set = _load_words(GlobalNames.REMOVE_WORDS_FILE)
    
    # Init jieba
    jieba.initialize()
    for w in user_define_words:
        jieba.add_word(w, freq=1000000)

    corpus_dict = None
    tfidf_model = None

    url_pattern = re.compile(r"(https|http)://.+?html")
    digit_pattern = re.compile(r"\d+")
    bracket_pattern = re.compile(r"\[.+?\]")

    not_place_set = set(["京东", "上门", "东西", "拜拜", "满意度",
        "新旧", "入口", "莫大", "蓝牙", "英伦", "顺顺利利",
        "哥哥", "立马", "海鲜", "回邮", "太多", "长北", "南那",
        "白跑", "天黑", "天阿", "美华", "华联", "日及", "山山",
        "京福顺", "卡拿", "太卡", "太大", "千古", "英哥", "两棵树",
        "太累", "包邮", "加半", "中华人名共和国", "六便士", "串联",
        "非顺丰", "中考", "北冰洋", "下嫩", "安安", "太鲜", "上拉",
        "入店", "上下水", "图京", "之城", "中断", "中武", "伦理", 
        "中道", "之康", "多维度", "黑边", "中爱", "之泰", "锦园店", 
        "三国", "阿门", "肯本", "刚京麦", "大黑", "朝霞", "关门大吉", 
        "哥别", "沧桑", "下山", "日京京", "沙沙", "牙牙", "顿顿", "山高",
        "钱和京", "非买", "上旧", "四科", "西东", "上岗", "大山", 
        "福尔马林", "滑黑", "上东", "中上", "内马尔", "中同", "中达",
        "下欧", "四门", "深春", "正东", "江南春", "入维", "大班", 
        "中联", "猫沙", "长卡", "几环", "尾塞", "小桥流水", "澳邮", 
        "上中", "英雄", "镇镇", "如东", "上口", "加邮", "八国", 
        "福利", "台基", "那本", "中邮", "六本", "维沙", "中黑", 
        "上美", "加花", "天哇", "远超过", "大拿", "贵干", "苏中",
        "三本", "酒塞", "七本", "美院", "中通", "美人壶加", "中充",
        "下国", "京伦", "九联", "上马", "美化", "江湖", "黑店", 
        "几米远", "午安", "七哥", "角美", "日春", "几比", "确保安全",
        "壶水", "荷塘月色", "云集", "拉边", "欧克", "中右", "加的京", 
        "上路", "烟嘴", "临证指南", "串口卡", "新建", "安利", "山泉水",
        "苏泊尔", "墨黑", "胶盆", "长达", "商城"])


    @classmethod
    def place_recognize(cls, text):
        places = [w for w, flag in pseg.cut(text) if "ns" in flag 
            and len(w) >= 2 
            and w not in cls.not_place_set 
            and "哈" not in w
            and "之" not in w 
            and "本" not in w
            and "中" not in w
            and "嫩" not in w
            and "大" not in w
            and "鲜" not in w
            and "国" not in w
            and "上" not in w
            and "确" not in w
            and "牙" not in w
            and "壶" not in w
            and "阿" not in w
            and "入" not in w
            and "哥" not in w
            and "颗" not in w
            and "的" not in w
            and "联" not in w
            and "哇" not in w]

        return places


    @classmethod
    def tokenize(cls,
                 text,
                 filter_punctuations=False,
                 filter_stopwords=False,
                 filter_alpha=False,
                 remove_words=False,
                 normalize_url=False,
                 recognize_place=False,
                 minimum_tokens_num=1): 
        '''Tokenize text'''
        try:
            places = cls.place_recognize(text)
            for w in places:
                text = text.replace(w, "[地址x]")
            text = cls.digit_pattern.sub("[数字x]", text)
            if normalize_url:
                text = cls.url_pattern.sub("URL", text)
            tokens = jieba.lcut(text)
            text = " ".join(tokens)
            for s in cls.bracket_pattern.findall(text):
                text = text.replace(s, s.replace(" ", ""))
            text = text.replace(u"# E - s [数字x]", u"#E-s[数字x]")
            text = text.replace(u"# E - s DIGIT [数字x]", u"#E-s[数字x]")
            text = text.replace(u"< s >", "<s>")
            tokens = text.split()
            tokens_copy = copy.copy(tokens)

            # Filter words.
            if filter_punctuations:
                tokens = [w for w in tokens if w not in cls.punctuations_set]
            if filter_stopwords:
                tokens = [w for w in tokens if w not in cls.stopwords_set]
            if filter_alpha:
                tokens = [w for w in tokens if not w.encode("utf-8").isalpha()
                    or w in set(["URL"])]
            if remove_words:
                tokens = [w for w in tokens if w not in cls.remove_words_set]

            if len(tokens) < minimum_tokens_num:
                tokens = tokens_copy

            new_tokens = tokens[:1]
            t_len = len(tokens)
            for i in range(1, t_len):
                if tokens[i] != tokens[i - 1]:
                    new_tokens.append(tokens[i])
            return new_tokens
        except Exception as e:
            print ("text=%s, errmsg=%s" % (text, e))
            return [text]


    @classmethod
    def get_tfidf(cls, words):
        if cls.tfidf_model is None:
            corpus_dict_path = get_file_path(GlobalNames.CORPUS_DICT_FILE)
            cls.corpus_dict = corpora.Dictionary.load(corpus_dict_path)
            corpus_tfidf_path = get_file_path(GlobalNames.CORPUS_TFIDF_FILE)
            cls.tfidf_model = models.tfidfmodel.TfidfModel.load(corpus_tfidf_path)
        bow = cls.corpus_dict.doc2bow(words)
        tfidf = cls.tfidf_model[bow]
        tfidf = [(cls.corpus_dict[x[0]], x[1]) for x in tfidf]
        tfidf.sort(key=lambda x: x[1], reverse=True)
        return tfidf
            

    @classmethod
    def get_keywords(cls, text, size=3, way=None):
        if way == None or way == "tfidf":
            tokens = cls.tokenize(text)
            tfidf = cls.get_tfidf(tokens)
            ret_tokens = [x[0] for x in tfidf[:size]]
            return ret_tokens
        elif way == "textrank":
            return jieba.analyse.textrank(text, topK=size)
