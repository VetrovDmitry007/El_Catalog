"""
Библиотека простых методов
"""

from flask import request

# mdc => 'werkzeug.datastructures.ImmutableMultiDict'
def f1(mdc):
    ls = []
    if mdc['edit_1'] != '': ls.append((mdc['select_1'], mdc['edit_1']))
    if mdc['edit_2'] != '': ls.append((mdc['select_2'], mdc['edit_2']))
    if mdc['edit_3'] != '': ls.append((mdc['select_3'], mdc['edit_3']))
    if mdc['edit_4'] != '': ls.append((mdc['select_4'], mdc['edit_4']))
    return ls
