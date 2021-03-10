"""
Библиотека простых методов
"""

import re
from App.ApiSQL import *
import tempfile
import os
import time
from threading import Thread
from App.from_pdf import save_PDF


# coding = UTF-8

def parsTeg(st):
    """
    Функция разбивает текст описани на тэги формата MARC
    :param st: Текст описания
    :return: Словарь вида {Тэг: Значение}
    """
    st = st.replace(u'\x1e', u' ')
    st = st.replace(u'\x1f', u'*+-')
    key = re.findall(r'\d{3,5}[ ]?[0-9]?[ ]?[*][+][-][a-z]', st)
    val = re.split(r'\d{3,5}[ ]?[0-9]?[ ]?[*][+][-][a-z]', st)
    val3 = []

    val = val[1::]
    for i in range(len(key)):
        val[i] = ''.join(list(key[i])[-4:]) + val[i]
        # key[i] = key[i][:-4]
        # Сократил тэг до 3-х симвадов
        key[i] = key[i][:-(len(key[i]) - 3)]

    ls = list(zip(key, val))
    dc = dict(ls)
    for i in dc.keys():
        key2 = re.findall(r'[*][+][-][a-z]', dc[i])
        val2 = re.split(r'[*][+][-][a-z]', dc[i])
        while '' in val2:
            val2.remove('')
        for j in range(len(key2)):
            key2[j] = key2[j].replace('*+-', '')
        for st in val2:
            val3.append(st.strip())
        ls2 = list(zip(key2, val3))
        dc[i] = dict(ls2)
        val3 = []
    dc_res = {}
    for k1, v1 in dc.items():
        for k2, v2 in v1.items():
            dc_res[k1 + k2] = v2
    return dc_res


def findBook(mdc):
    """
    Поиск книг в форме поиска
    :param mdc: => 'werkzeug.datastructures.ImmutableMultiDict'
    :return: Список ID найденных книг
    """
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
        ['Выходные данные', (dc_tag.get('260a', '_') + ' ' + dc_tag.get('260b', '') + ' ' + dc_tag.get('260c', ''))],
        ['Источник информации',
         (dc_tag.get('773t', '_') + ' ' + dc_tag.get('773d', '') + ' ' + dc_tag.get('773g', ''))],
        ['Ключевые слова', dc_tag.get('653a', None)],
        ['Объём', dc_tag.get('300a', None)],
        ['Макрообъект', dc_tag.get('900a', None)],
    ]

    ls_result = [st for st in ls_result if st[1] is not None]
    ls_result = [st for st in ls_result if len(st[1]) > 3]
    return ls_result


def uploadFile(book_id):
    """
    Создаем временный файл макрообъекта
    :param book_id: ID книги
    :return: кортэж (fd - Дескриптор файла, path - Полное имя файла)
    """
    if book_id is None:
        return None
    # Устанавливаем каталог программы
    dir_prog = os.path.dirname(os.path.abspath(__file__))
    os.chdir(dir_prog)
    marc = Class_Sql()
    data, xtd = marc.loadFromSql(book_id)
    if data is None:
        return None
    # создаем временный файл
    fd, path = tempfile.mkstemp(suffix='.' + xtd, text=True, dir='upload')
    # print('создаем временный файл:', path)
    with open(path, 'wb') as f:
        f.write(data)
    return fd, path


def uploadPDF(ls_book):
    """
    Создаёт временный PDF файл (результат поиска)
    :param ls_book: Список книг
    :return: кортэж (fd - Дескриптор файла, path - Полное имя файла)
    """
    # Устанавливаем каталог программы
    dir_prog = os.path.dirname(os.path.abspath(__file__))
    os.chdir(dir_prog)
    # создаем временный файл
    fd, path = tempfile.mkstemp(suffix='.pdf', text=True, dir='upload')
    save_PDF(ls_book=ls_book, name_pdf=path)
    return fd, path


def delTemFile(fd, path):
    """
    Функция для запуска в потоке
    Через промежуток времени tim удаляет вменный файл
    :param fd: Дескриптор файла
    :param path: Полное имя файла
    :return:
    """
    print('Запуск удаления:', path)
    tim = 30
    time.sleep(tim)
    # закрываем дескриптор файла
    os.close(fd)
    # уничтожаем файл
    os.unlink(path)
    print('Удален:', path)


def StartThreadDel(fd, path):
    """
    Запуск потока обработки удаления временного файла
    :param fd: Дескриптор файла
    :param path: Полное имя файла
    :return:
    """
    thread = Thread(target=delTemFile, args=(fd, path,))
    thread.start()


if __name__ == '__main__':
    # from pprint import pprint
    marc = Class_Sql()
    txt_book = marc.getOneBook(17822)
    # dc = parsTeg(txt_book)
    # pprint(dc)
