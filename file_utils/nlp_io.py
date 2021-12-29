# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   Description :  
   Author :        kedaxia
   date：          2021/12/29
   Copyright:      (c) kedaxia 2021
-------------------------------------------------
   Change Activity:
                   2021/12/29: 
-------------------------------------------------
"""


def save_to_BIO(word_lists,labels,file_path):
    '''
    这就是将格式转变为BIO格式，一行：word \t label
    这时 word_lists和label是完全一一对应的,句子以空格分开....
    :param word_lists:
    :param labels:
    :return:
    '''
    res = []
    for a, b in zip(word_lists, labels):
        if a == ' ' and b == ' ':
            res.append('\n')
        else:
            res.append("{} {}\n".format(a, b))

    f = open(file_path,'w',encoding='utf-8')
    f.writelines(res)
    f.close()
