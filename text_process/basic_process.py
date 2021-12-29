# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   Description :  
   Author :        kedaxia
   date：          2021/12/28
   Copyright:      (c) kedaxia 2021
-------------------------------------------------
   Change Activity:
                   2021/12/28: 
-------------------------------------------------
"""


def get_entity_in_sentence_id(start_idx,end_idx, sentence_boundary):
    '''
    根据一个单词单词在raw_text的start_offset和end_offset范围来得到这个单词在第几个句子里
    常用于关系分类任务...

    :param end_idx:
    :return:
    '''

    for idx, tmp_idx in enumerate(sentence_boundary):
        sentence_start, sentence_end = tmp_idx
        if sentence_start <= start_idx <= end_idx <= sentence_end:
            return idx

    raise ValueError("出错了")



def get_origin_to_new_index(raw_text,tokenize_words):
    '''
    将tokenize_words与raw_text的字符级别index进行对照，形成映射点到点的映射
    :param tokenize_word:
    :param abstract_text:
    :return: 返回两个字典
    '''
    # raw_text的index对应
    raw_index_to_tokenize_index = {}

    start1 = 0
    start2 = 0
    tokenize_text = "".join(tokenize_words)
    while start1<len(raw_text) and start2<len(tokenize_text):
        while start1<len(raw_text) and start2<len(tokenize_text) and raw_text[start1] != tokenize_text[start2]:
            start1 += 1

        while start1<len(raw_text) and start2<len(tokenize_text) and raw_text[start1] == tokenize_text[start2]:
            raw_index_to_tokenize_index[start2] = start1
            start1 += 1
            start2 += 1
    tokenize_index_to_raw_index =  {value:key for key,value in raw_index_to_tokenize_index.items()}
    return raw_index_to_tokenize_index,tokenize_index_to_raw_index


def find_entity_sentence_id(start_idx,end_idx, sentence_boundary):
    '''
    这是获得当前实体在abstract中的第几个句子，即序列号
    其实，一般实体都是出现在一个句子之中，因此，主要是
    :param entities: 这里使用无需转换的idx，skr
    :param end_idx:
    :return:
    '''


    for idx, tmp_idx in enumerate(sentence_boundary):
        sentence_start, sentence_end = tmp_idx
        if sentence_start <= start_idx <= end_idx <= sentence_end:
            return idx

    raise ValueError("没有找到这个单词在哪个句子中...")


def find_entity_word_id(start_idx,end_idx, word_boundary):
    '''

    主要是将entities的offset从char-level转变为word-level的index...，

    这是转变为BIO格式的关键一步，一个word对应一个label...

    :param entities:
    :param sentence_li:
    :return:
    '''
    idx = 0
    while idx < len(word_boundary):
        s1, e1 = word_boundary[idx]
        if start_idx == s1 and end_idx == e1:  # 实体是一个单词的情况
            return (idx, idx)
        elif start_idx == s1 and end_idx != e1:  # 实体多个单词组成
            tmp_start = idx

            while idx < len(word_boundary):
                s1, e1 = word_boundary[idx]
                if end_idx != e1:
                    idx += 1
                else:
                    tmp_end = idx
                    return (tmp_start, tmp_end)

            raise ValueError("没有找到当前word在tokenize word的位置，这可能是分词导致的错误....")

        else:
            idx += 1
    raise ValueError("没有找到当前word在tokenize word的位置，这可能是分词导致的错误....")



def get_word_boundary(raw_text,tokenize_word):
    '''
    相当于得到每个单词在raw_text的index
    :param tokenize_word:
    :param abstract_text:
    :return:
    '''
    word_boundary = []

    start2 = 0
    text_len = len(raw_text)

    for idx, word in enumerate(tokenize_word):

        if word == '``':
            raise ValueError

        while start2 < text_len and raw_text[start2] != word[0]:
            start2 += 1

        start1 = start2
        word_start = 0
        while word_start < len(word) and start2 < text_len and raw_text[start2] == word[word_start]:
            start2 += 1
            word_start += 1

        if start2 >= text_len:
            word_boundary.append((start1, start2))
            break
        word_boundary.append((start1, start2))

    return word_boundary


def get_sentence_boundary(raw_text, sentence_li):
    '''
    给定一个文档和文档中的各个句子
    得到每个句子在raw_text的index范围
    :param raw_text:
    :param sentence_li:
    :return: sentence_boundary
        [(0,12),(13,15),...]
    '''
    sentence_boundary = []
    # 这个就是
    start2 = 0

    text_len = len(raw_text)
    for idx, sentence in enumerate(sentence_li):

        while start2 < text_len and raw_text[start2] != sentence[0]:
            start2 += 1

        start1 = start2
        word_start = 0
        while word_start < len(sentence) and start2 < text_len and raw_text[start2] == sentence[word_start]:
            start2 += 1
            word_start += 1

        if start2 >= text_len:
            sentence_boundary.append((start1, text_len))
            break
        sentence_boundary.append((start1, start2))

    return sentence_boundary