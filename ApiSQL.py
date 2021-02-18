import pyodbc
import random
from sys import platform

class Class_Sql:

    def __init__(self):
        if platform == 'linux':
            self.cnxn = pyodbc.connect(
                'DRIVER=FreeTDS; SERVER=172.16.157.1; PORT=1433; DATABASE=rb_mar; UID=sa; PWD=sql_admin; TDS_Version=8.0;')
        else:
            self.cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=172.16.157.1;DATABASE=rb_mar;UID=sa;PWD=sql_admin')


    def getIdBook(self, tag, val_tag, prec = True):
        """
        Список DOC_ID найденных книг
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
        cursor.execute(sql)
        row = cursor.fetchall()
        ls = [col[0] for col in row]
        return ls

    def listBook(self, ls_id):
        """
        Сисок книг по списку их id
        :param ls_id:
        :return: <class: list>
        """
        cursor = self.cnxn.cursor()
        # sql = f"SELECT IDX{tag}X.DOC_ID FROM IDX{tag}, IDX{tag}X where IDX{tag}.IDX_ID = IDX{tag}X.IDX_ID and IDX{tag}.TERM like '{val_tag}%'"
        ls_id = list(map(str, ls_id))
        str_id = ','.join(ls_id)
        sql = f"SELECT ITEM FROM DOC where DOC_ID in ({str_id})"
        print(sql)
        cursor.execute(sql)
        row = cursor.fetchall()
        ls_book = [col[0] for col in row]
        return ls_book

    def getRnd(self, tag):
        """
        Выбор рандомной записи из словаря
        :param tag: Тэг (100a or 245a or ... )
        :return: Рандомная запись
        """
        cursor = self.cnxn.cursor()
        sql = f'SELECT min(IDX_ID) as min_row, max(IDX_ID) as max_row FROM IDX{tag}'
        cursor.execute(sql)
        row = cursor.fetchall()
        min_id, max_id = row[0][0], row[0][1]
        random.seed(random.randint(1,100))
        # random.seed(1)
        rnd_id = random.randint(min_id, max_id)
        sql = f"SELECT TERM FROM IDX{tag} where IDX_ID = {rnd_id}"
        cursor.execute(sql)
        row = cursor.fetchall()
        return row[0][0]


if __name__ == '__main__':
    from pprint import pprint
    marc = Class_Sql()
    print(marc.getRnd('100a'))
    print(marc.getRnd('100a'))
    print(marc.getRnd('100a'))

