import fpdf
import re


def made_pdf(list_book, name_pdf):
    pdf = fpdf.FPDF(format='legal')  # pdf format
    pdf.add_page()
    pdf.add_font('DejaVu_Bold', '', './Font/DejaVuSans-Bold.ttf', uni=True)
    pdf.set_font('DejaVu_Bold', '', 12)
    pdf.cell(15, 10, txt='Библиографическое описание', ln=1)
    pdf.set_font('DejaVu_Bold', '', 10)
    pdf.cell(65, 10, txt='Поле')
    pdf.cell(15, 10, txt='Значение', ln=1)
    pdf.cell(50, 7, txt='', ln=1)
    pdf.add_font('DejaVu', '', './Font/DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 10)
    pdf.set_line_width(0.5)
    pdf.set_draw_color(0, 0, 0)
    pdf.line(11, 30, 202, 30)

    for list_el in list_book:
        pdf.cell(65, 5, txt=list_el[0])
        st2 = list_el[1]
        while len(st2) > 60:
            st = st2[:60]
            st = re.split(r'\W', st)
            del st[-1]
            st2 = re.split(r'\W', st2)
            for el in range(len(st)):
                del st2[0]
            st = ' '.join(st).strip()
            st2 = ' '.join(st2).strip()
            pdf.cell(15, 5, txt=st, ln=1)
            pdf.cell(65, 5, txt='')
            list_el[1] = st2

        pdf.cell(15, 5, txt=list_el[1])
        pdf.cell(0, 8, txt='', ln=1)

    pdf.output(name_pdf)
    return True

if __name__ == '__main__':
    ls = [['Индекс УДК', '633.2/.4+ 908'], ['Каталожный индекс', '633.2/.4+'], ['Автор', 'Парахин, Н. В.'], ['Заглавие', 'Эколого-стабилизирующее значение кормовых культур в растениеводстве'], ['Аннотация', 'Оценено влияние кормовых культур на устойчивость агроландшафтов и продуктивность растений.С точки зрения экологического земледелия обоснована необходимость размещения и оптимизации посевов кормовых культур в структуре севооборота.Проанализированы результаты многочисленных опытов,в постановке которых участвовал автор.На примере Орловской области предложены направления выхода из кризисного положения отрасли растениеводства с учетом использования биологических особенностей кормовых культур'], ['Основная рубрика', 'Краеведение'], ['Выходные данные', 'М. Колос 1997'], ['Ключевые слова', 'Культуры кормовые в воспроизводстве плодородия почвы'], ['Объём', '176с.']]
    print(made_pdf(ls, 'Test.pdf'))