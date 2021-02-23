"""
Библиотека простых методов
"""

import re
from flask import request
from ApiSQL import *


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
    """
    Функция разбивает текст описани на тэги формата MARC
    :param st: Текст описания
    :return: Словарь вида {Тэг: Значение}
    """
    st = st.replace(u'\x1e', u' ')
    st = st.replace(u'\x1f', u'')
    key = re.findall(r'\d{3,5}[ ]?[0-9]?[ ]?[a-z]', st)
    val = re.split(r'\d{3,5}[ ]?[0-9]?[ ]?[a-z]', st)
    val3 = []

    for i in range(len(key)):
        val[i] = list(key[i])[-1] + val[i]
        # key[i] = key[i][:-1]
        # Сократил тэг до 3-х симвадов
        key[i] = key[i][:-(len(key[i]) - 3)]

    val = val[1::]
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


def findBook(mdc):
    """
    Поиск книг в форме поиска
    :param mdc: => 'werkzeug.datastructures.ImmutableMultiDict'
    :return: Список ID найденных книг
    """
    dc = {}
    if mdc['edit_1'] != '': dc[mdc['select_1']] = mdc['edit_1']
    if mdc['edit_2'] != '': dc[mdc['select_2']] = mdc['edit_2']
    if mdc['edit_3'] != '': dc[mdc['select_3']] = mdc['edit_3']
    if mdc['edit_4'] != '': dc[mdc['select_4']] = mdc['edit_4']

    ls_id = []
    marc = Class_Sql()
    ls_id.extend([marc.getIdBook(key, val) for key, val in dc.items()])

    return ls_id[0]



if __name__ == '__main__':
    from pprint import pprint
    # ls = crSpisBook(50)
    # pprint(ls)
    marc = Class_Sql()
    txt_book = marc.getOneBook(173833)
    print(txt_book)
    # print(parsTeg('001  0RU/IS/BASE/339260830005  020101001150710.302000c0-1004000eИшханова09000a636.8xЕ 47wЦФeб/нfЦФ-1б/н09400aП2001(ЦФ)09700a900bИшханова_Е10010aЕлагин Л.А.24500aКролик,его мясо,мех,пух и шерсть.26000aПетроградbГос.типографияc191930000a50с650 4aКролиководство65300aМясо кролика65300aПороды кроликов65300aПомещение для кроликов 65300aКормление кроликов65300aРазмножение кроликов65300aСодержание кроликов65300aУбой кроликов65300aБолезни кроликов; Ресурс электронный; Макрообъект900  aЕлагин Л. Н. Кролик99000z0j1'))
    pprint(parsTeg(txt_book))