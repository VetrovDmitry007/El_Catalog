import os

import pyodbc
import random
from sys import platform

class Class_Sql:

    def __init__(self):
        dir_prog = os.path.dirname(os.path.abspath(__file__))
        os.chdir(dir_prog)
        if platform == 'linux':
            self.cnxn = pyodbc.connect(
                'DRIVER=FreeTDS; SERVER=172.16.157.1; PORT=1433; DATABASE=rb_mar; UID=sa; PWD=sql_admin; TDS_Version=8.0;')
        else:
            self.cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=172.16.157.1;DATABASE=rb_mar;UID=sa;PWD=sql_admin')


    def getIdBook(self, tag, val_tag, prec = False):
        """
        Поиск книги по словарю
        :param tag: Тэг поля книги (100а, 245a, ...)
        :param val_tag: Значение поля
        :param prec: Точное совпадение (True / False)
        :return: Список DOC_ID
        """
        "FROM IDX100a where TERM like '%Аббасов%' and TERM like '%Т.%' and TERM like '%Г.%'"
        cursor = self.cnxn.cursor()
        sql_prec = f"SELECT IDX{tag}X.DOC_ID FROM IDX{tag}, IDX{tag}X where IDX{tag}.IDX_ID = IDX{tag}X.IDX_ID and IDX{tag}.TERM = '{val_tag}'"
        sql_approx = f"SELECT IDX{tag}X.DOC_ID FROM IDX{tag}, IDX{tag}X where IDX{tag}.IDX_ID = IDX{tag}X.IDX_ID and IDX{tag}.TERM like '{val_tag}%'"
        sql = sql_prec if prec else sql_approx
        print(sql)
        cursor.execute(sql)
        row = cursor.fetchall()
        ls = [col[0] for col in row]
        return ls

    def getValTeg(self, tag, book_id):
        """
        Возвращает значение тэка указанной книги
        :param teg: Тэг поля
        :param book_id: Id книги
        :return: Значение тэга
        """
        cursor = self.cnxn.cursor()
        sql = f"SELECT IDX{tag}.TERM FROM IDX{tag}X, IDX{tag} where IDX{tag}X.DOC_ID = {book_id} and IDX{tag}X.IDX_ID = IDX{tag}.IDX_ID"
        cursor.execute(sql)
        row = cursor.fetchall()
        ls = [col[0] for col in row]
        s = ls[0].replace('<null>','')
        return s


    def listBook(self, ls_id):
        """
        !!! Пока не используем
        Сисок книг по списку их id
        :param ls_id:
        :return: <class: list>
        !!! Должно взвращать опискние книги для его парсинга
        """
        cursor = self.cnxn.cursor()
        # sql = f"SELECT IDX{tag}X.DOC_ID FROM IDX{tag}, IDX{tag}X where IDX{tag}.IDX_ID = IDX{tag}X.IDX_ID and IDX{tag}.TERM like '{val_tag}%'"
        ls_id = list(map(str, ls_id))
        str_id = ','.join(ls_id)
        sql = f"SELECT ITEM FROM DOC where DOC_ID in ({str_id})"
        cursor.execute(sql)
        row = cursor.fetchall()
        ls_book = [col[0] for col in row]
        return ls_book

    def getOneBook(self, book_id):
        """
        Возвращает библиографическое описание книги
        :param book_id: ID книги
        :return: Библиографическое описание книги
        """
        cursor = self.cnxn.cursor()
        sql = f"SELECT ITEM FROM DOC where DOC_ID in ({book_id})"
        cursor.execute(sql)
        row = cursor.fetchall()
        txt_book = [col[0] for col in row][0]
        return txt_book

    def getSpisBook(self, ls_id):
        """
        Возвращает список найденных книг
        :param ls_id: Список ID книг
        :return: список словарей (автор, заглавие, издательство, объём)
        """
        ls = []
        for id in ls_id:
            dc = {}
            src = self.getValTeg('260b', id) if bool(self.getValTeg('260b', id).strip()) else self.getValTeg('773t', id) # Издательство / Источник
            v_book = self.getValTeg('300a', id) if bool(self.getValTeg('300a', id).strip()) else self.getValTeg('773g', id) # Объём
            macro = 'Есть' if len(self.getValTeg('900a', id)) > 1 else ""
            dc.update({'id': id, '100a': self.getValTeg('100a', id), '245a': self.getValTeg('245a', id), '260b': src, '300a': v_book,'900a': macro})
            ls.append(dc)
        return ls


    def loadFile(self, book_id):

        mcr_name = self.getValTeg('900a', book_id)
        print(mcr_name)
        cursor = self.cnxn.cursor()
        # sql = f"SELECT ITEM FROM MOBJECT where NAME = '{mcr_name}'"
        sql = f"SELECT ITEM FROM MOBJECT where NAME = 'Финансы и кредит 12-2'"
        cursor.execute(sql)
        row = cursor.fetchall()
        data = row[0][0]
        # print(type(data))
        with open('./upload/test.pdf', 'wb') as f:
            f.write(data)

"""
SELECT ITEM FROM MOBJECT where NAME =
"""

if __name__ == '__main__':
    from pprint import pprint
    marc = Class_Sql()
    # print(marc.getIdBook('245a', 'Кролики'))
    # print(marc.listBook([173833, 277715, 170115, 113161, 39410]))
    # print(marc.getValTeg('260b', 173833))
    # print(marc.getOneBook(173833))

    marc.loadFile(333257)




