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
import string
import re
def re_tokenize(raw_text):
    '''

    使用正则表达式将文本切割为word-level
    :param raw_text:
    :return:
    '''

    tokenize_words = [x.strip() for x in re.split(r'(\w+)?', raw_text) if x and x != ' ']

    return tokenize_words

def char_tokenize(text_li):
    '''
    这里以句子为单位进行合并，只要是一段连续的字母或者数字，将空格和特殊符号之间的就合并....
    :param text_li:
    :return:
    '''
    tmp_text_li = []
    p1 = 0
    p2 = 0
    lens = len(text_li)
    while p1<lens and p2<lens:
        while p2<lens and text_li[p2].lower() in string.ascii_lowercase:
            p2 += 1

        tmp_text_li.append(''.join(text_li[p1:p2]))

        while p2<lens and text_li[p2].lower() not in string.ascii_lowercase:
            tmp_text_li.append(text_li[p2])
            p2 += 1
        p1 = p2
    #tmp_text_li = [x for x in tmp_text_li if x != ' ']

    return tmp_text_li




if __name__ == '__main__':
    s = 'Binding of factor Xa to human umbilical vein endothelial cells (HUVEC) is contributed by effector cell protease receptor-1 (EPR-1). The structural requirements of this recognition were investigated.'
    tokenize_s = char_tokenize(list(s))
    print(tokenize_s)
    print('--')
