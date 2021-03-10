import fpdf
import re


def save_PDF(ls_book, name_pdf):
    """

    :param ls_book: Список книг
    :return:
    """
    # print(ls_book)
    ls = [7, 35, 70, 65, 15]
    ls_k = [7, 35, 70, 65, 15]
    raz = ' '
    word_ls = []
    num = 0
    fr = 0
    cn = -1
    fl = 0
    ls3 = []
    max_ls = []
    cn3 = -1
    sch = 0

    pdf = fpdf.FPDF(format='legal')  # pdf format
    pdf.add_page()
    pdf.add_font('DejaVu_Bold', '', 'DejaVuSans-Bold.ttf', uni=True)
    pdf.set_font('DejaVu_Bold', '', 10)
    pdf.cell(7, 10, txt='#')
    pdf.cell(35, 10, txt='Автор')
    pdf.cell(70, 10, txt='Заглавие')
    pdf.cell(65, 10, txt='Издательство')
    pdf.cell(15, 10, txt='Объём', ln=1)
    pdf.cell(50, 7, txt='', ln=1)
    pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 10)
    pdf.set_line_width(0.5)
    pdf.set_draw_color(0, 0, 0)
    pdf.line(11, 20, 202, 20)

    # Для исправленея ошибки переполнения списка
    # if len(ls_book) > 47:
    #     ls_book = ls_book[:47]

    for dc_teg in ls_book:
        for j in dc_teg.items():
            if str(j[0]) == 'id':
                num += 1
                word_ls.append(str(num))
            if str(j[0]) != 'id' and str(j[0]) != '900a':
                st = j[1]
                while len(st) > 30:
                    fr += 1
                    st1 = st[:30]
                    st = re.split(r'\W', st)
                    st1 = re.split(r'\W', st1)
                    del st1[-1]
                    for x in range(len(st1)):
                        del st[0]
                    st1 = ' '.join(st1)
                    st = ' '.join(st)
                    if fr == 1:
                        word_ls.append([st1])
                    else:
                        word_ls[-1].append(st1)
                    fl = 1

                if j[0] == '100a' and len(st) >= 17:
                    word_ls.append(st.split(','))
                elif fl != 1:
                    word_ls.append(st)
                else:
                    word_ls[-1].append(st)
                fr = 0
                fl = 0

    for i in range(len(word_ls) + 1):
        cn += 1
        if cn == 5:
            for x in ls3:
                if type(x) == list:
                    max_ls.append(len(x))
            if len(max_ls) > 0:
                max_ch = max(max_ls) - 1
            else:
                max_ch = 0
            for j in range(max_ch):
                sch += 1
                pdf.cell(0, 5, txt='', ln=1)
                for y in ls3:
                    cn3 += 1
                    if cn3 == 5:
                        cn3 = 0
                    try:
                        if type(y) == list:
                            pdf.cell(ls_k[cn3], 2, txt=y[sch].strip())
                        else:
                            pdf.cell(ls_k[cn3], 0, txt='')
                    except:
                        cn3 = -1
                        break
            cn3 = -1
            sch = 0
            pdf.cell(0, 10, txt = '', ln = 1)
            max_ls = []
            max_ch = 0
            ls3 = []
            cn = 0
        try:
            if type(word_ls[i]) == list:
                pdf.cell(ls[cn], 3, txt=word_ls[i][0])
            else:
                pdf.cell(ls[cn], 3, txt=word_ls[i])
            ls3.append(word_ls[i])
        except:
            break

    pdf.output(name_pdf)
    return True


if __name__ == '__main__':
    dk = [{'id': 170115, '100a': 'Калугин, Ю. А.', '245a': 'Кролики и зайцы - родственники, но не близкие', '260b': 'Кролиководство и звероводство', '300a': 'С. 18-20', '900a': ''},
          {'id': 173833, '100a': 'Кашкаров, А.', '245a': 'Кролики "выбирают" свободу', '260b': 'Информационный бюллетень', '300a': 'С. 47-48', '900a': ''},
          {'id': 113161, '100a': ' ', '245a': 'Кролики растут быстрее', '260b': 'Крестьянские ведомости', '300a': 'С. 23', '900a': ''},
          {'id': 39410, '100a': 'Житникова, Ю.', '245a': 'Кролики.Разведение,содержание,переработка мяса,выделка шкурок', '260b': 'Феникс', '300a': '320с', '900a': ''},
          {'id': 277715, '100a': 'Политова, М.', '245a': 'Кролики без фокусов', '260b': 'Новое сельское хозяйство', '300a': 'С. 22-26', '900a': ''}]
    a = save_PDF(dk, 'Temp.pdf')
    print(a)
