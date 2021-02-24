"""
Библиотека простых методов
"""

import re
from flask import request
from ApiSQL import *

# coding = UTF-8

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
    # Убираем вложенность словаря
    dc_res = {}
    for k1, v1 in dc.items():
        for k2, v2 in v1.items():
            dc_res[k1+k2] = v2
    return dc_res


def findBook(mdc):
    """
    Поиск книг в форме поиска
    :param mdc: => 'werkzeug.datastructures.ImmutableMultiDict'
    :return: Список ID найденных книг
    """
    tag = []
    marc = Class_Sql()

    set_full, set_id_2, set_id_3, set_id_4 = set(), set(), set(), set()

    if mdc['edit_1'] != '':
        tag = [mdc['select_1'], mdc['edit_1']]  # {'100a': 'Иванов'}
        set_full = set(marc.getIdBook(tag[0], tag[1]))

    if mdc['edit_2'] != '':
        tag = [mdc['select_2'], mdc['edit_2']]
        set_id_2 = set(marc.getIdBook(tag[0], tag[1]))
        if mdc['select_2_0'] == 'ИЛИ':
            set_full = set_full | set_id_2
        else:
            set_full = set_full & set_id_2

    if mdc['edit_3'] != '':
        tag = [mdc['select_3'], mdc['edit_3']]
        set_id_3 = set(marc.getIdBook(tag[0], tag[1]))
        if mdc['select_3_0'] == 'ИЛИ':
            set_full = set_full | set_id_3
        else:
            set_full = set_full & set_id_3

    if mdc['edit_4'] != '':
        tag = [mdc['select_4'], mdc['edit_4']]
        set_id_4 = set(marc.getIdBook(tag[0], tag[1]))
        if mdc['select_4_0'] == 'ИЛИ':
            set_full = set_full | set_id_4
        else:
            set_full = set_full & set_id_4

    return set_full


def getInfoBook(book_id):
    marc = Class_Sql()
    txt_book = marc.getOneBook(book_id)
    dc_tag = parsTeg(txt_book)
    ls_result = [
                  ['Индекс УДК', dc_tag.get('080a', None)],
                  ['Каталожный индекс', dc_tag.get('090c', None)],
                  ['Автор', dc_tag.get('100a', None)],
                  ['Другие авторы', dc_tag.get('700a', None)],
                  ['Заглавие', dc_tag.get('245a', None)],
                  ['Продолжение заглавия', dc_tag.get('245b', None)],
                  ['Аннотация', dc_tag.get('520a', None)],
                  ['Основная рубрика', dc_tag.get('650a', None)],
                  ['Выходные данные', (dc_tag.get('260a', '_')+' '+dc_tag.get('260b', '')+' '+dc_tag.get('260c', '')) ],
                  ['Источник информации', (dc_tag.get('773t', '_')+' '+dc_tag.get('773d', '')+' '+dc_tag.get('773g', '')) ],
                  ['Ключевые слова', dc_tag.get('653a', None)],
                  ['Объём', dc_tag.get('300a', None)],
                  ['Макрообъект', dc_tag.get('900a', None)],
                  ]

    ls_result = [st for st in ls_result if st[1] != None]
    ls_result = [st for st in ls_result if len(st[1]) > 3]
    return ls_result

if __name__ == '__main__':
    from pprint import pprint
    marc = Class_Sql()
    txt_book = marc.getOneBook(17822)
    dc = parsTeg(txt_book)
    pprint(dc)
