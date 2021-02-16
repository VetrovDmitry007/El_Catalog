import pyodbc

class Class_Sql:

    def __init__(self):
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


if __name__ == '__main__':
    from pprint import pprint
    marc = Class_Sql()
    # ls_id = marc.getIdBook('100a', 'Аббасов, Т. Г.')
    ls_id = marc.getIdBook('245a', 'Теория механизмов и машин')
    # ls_id = marc.getIdBook('245a', 'Экономика')

    print(ls_id)
    ls_book = marc.listBook(ls_id)
    pprint(ls_book)
