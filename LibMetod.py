"""
Библиотека простых методов
"""

import re
from pprint import pprint
from flask import request
from ApiSQL import *

def parsFind(mdc):
    """
    Разбор данных пересланных формой поиска
    :param mdc: => 'werkzeug.datastructures.ImmutableMultiDict'
    :return: данные для поиска <class: list>
    """
    ls = []
    if mdc['edit_1'] != '': ls.append((mdc['select_1'], mdc['edit_1']))
    if mdc['edit_2'] != '': ls.append((mdc['select_2'], mdc['edit_2']))
    if mdc['edit_3'] != '': ls.append((mdc['select_3'], mdc['edit_3']))
    if mdc['edit_4'] != '': ls.append((mdc['select_4'], mdc['edit_4']))
    return ls

def crSpisBook(cn):
    """
    !! Random НЕ работает
    Создание тестового списка книг
    :param cn: размер итогового списка
    :return: список словарей (автор, заглавие, издательство, объём)
    """
    marc = Class_Sql()
    ls = []
    dc = {}
    for _ in range(cn):
        # dc.update({'100a': marc.getRnd('100a'), '245a': marc.getRnd('245a'), '260b': marc.getRnd('260b'), '300a': random.randint(100, 900), })
        dc.update({'id': 526, '100a': marc.getRnd('100a'), '245a': marc.getRnd('245a'), '260b': 'Машиностроение', '300a': random.randint(100, 900), })
        ls.append(dc)
    return ls

def parsTeg(st):
    st = st.replace(u'\x1e', u' ')
    st = st.replace(u'\x1f', u'')
    key = re.findall(r'\d{3,5}[ ]?[0-9]?[ ]?[a-z]', st)
    val = re.split(r'\d{3,5}[ ]?[0-9]?[ ]?[a-z]', st)
    val3 = []

    val = val[1::]
    for i in range(len(key)):
        val[i] = list(key[i])[-1] + val[i]
        # key[i] = key[i][:-1]
        # Сократил тэг до 3-х симвадов
        key[i] = key[i][:-(len(key[i]) - 3)]

    ls = list(zip(key, val))
    dc = dict(ls)
    for i in dc.keys():
        key2 = re.findall(r'[a-z]', dc[i])
        val2 = re.split(r'[a-z]', dc[i])
        while '' in val2:
            val2.remove('')
        for st in val2:
            val3.append(st.strip())
        ls2 = list(zip(key2, val3))
        dc[i] = dict(ls2)
        val3 = []
    return dc




if __name__ == '__main__':
    # from pprint import pprint
    # ls = crSpisBook(50)
    # pprint(ls)

    pprint(parsTeg('001  0RU/IS/BASE/358335742005  020110510094431.4090  c636.92100  aКашкаров, А.245  aКролики "выбирают" свободу65014aКролиководство653  aСодержание кроликов бесклеточное773  tИнформационный бюллетеньd2011. - N 1gС. 47-48'))