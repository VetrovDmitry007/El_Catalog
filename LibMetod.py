"""
Библиотека простых методов
"""

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




if __name__ == '__main__':
    from pprint import pprint
    ls = crSpisBook(50)
    pprint(ls)