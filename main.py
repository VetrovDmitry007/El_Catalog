import json

from flask import Flask, render_template, session, send_file, request, redirect, url_for
from App.LibMetod import *
from App import ec_cfg
from App.Forms import LoginForm, FindForm, HideForm

app = Flask(__name__, static_folder='static')
app.debug = ec_cfg.debugFlask
app.config['SECRET_KEY'] = ec_cfg.SECRET_KEY
# отключить кэш CSS
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/MarcWeb/Work.asp')
@app.route('/')
def index():
    """
    Возвращает форму авторизации пользователя
    :return: Форма авторизации
    """
    login_form = LoginForm()
    return render_template('authorize.html', form=login_form)


@app.route('/MarcWeb/exit')
@app.route('/exit')
def session_exit():
    session.clear()
    return redirect(url_for('index'))


@app.route('/MarcWeb/login', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def authoriz():
    """
    После авторизации возвращает форму поиска
    :return: Форма поиска
    """
    find_form = FindForm()
    login_form = LoginForm()
    if login_form.validate_on_submit():
        session['login'] = login_form.username.data
        session['psw'] = login_form.password.data
        if ('psw' in session) and (session["psw"].strip() == ec_cfg.pswMarc) and (
                session["login"].strip() == ec_cfg.loginMarc):
            return render_template('find.html', form=find_form)
    return redirect(url_for('index'))


@app.route('/MarcWeb/f_find', methods=['GET', 'POST'])
@app.route('/f_find', methods=['GET', 'POST'])
def getFrmFind():
    """
    Возвращает форму поиска
    :return: Форма поиска
    """
    find_form = FindForm()
    return render_template('find.html', form=find_form)


@app.route('/MarcWeb/find', methods=['POST'])
@app.route('/find', methods=['POST'])
def find():
    """
    Возвращает список найденной литературы
    :return: Список словарей
    """
    if ('psw' in session) and (session["psw"].strip() == ec_cfg.pswMarc) and (
            session["login"].strip() == ec_cfg.loginMarc):
        """
        Добавить поиск и удаление файлов старше одного часа
        """
        # Получаем элементы формы и формируем список книг
        find_form = FindForm()
        ls_id = findBook(find_form)
        marc = Class_Sql()
        ls_book = marc.getSpisBook(ls_id)
        # Список -> json -> Скрытый элемент формы
        hide_form = HideForm()
        hide_form.json_txt.data=json.dumps(ls_book)
        return render_template('tabResult.html', ls_book=ls_book, form=hide_form)
    return redirect(url_for('index'))


@app.route('/MarcWeb/book/<id>')
@app.route('/book/<id>')
def infoBook(id):
    """
    Возвращает библиографическое описание книги
    :param id: ID книги
    :return: Форма библиографическое описание книги
    """
    if ('psw' in session) and (session["psw"].strip() == ec_cfg.pswMarc) and (
            session["login"].strip() == ec_cfg.loginMarc):
        ls_tag = getInfoBook(id)
        print('Биб. описание', ls_tag)
        return render_template('infoBook.html', ls_tag=ls_tag, book_id=id)
    return redirect(url_for('index'))


@app.route('/MarcWeb/upload/<book_id>')
@app.route('/upload/<book_id>')
def upload_file(book_id):
    """
    Выгрузка пользователю макрообъекта
    :param book_id: ID книги
    :return: Файл макрообъекта
    """
    tpl = uploadFile(book_id)  # кортэж (fd, path)
    if tpl:
        fd, path = tpl
        StartThreadDel(fd, path)
        return send_file(path)  # посмотреть справку по send_file()
    # если файл макрообъекта не создан
    return redirect(url_for('getFrmFind'))


@app.route('/MarcWeb/result_find')
@app.route('/result_find')
def return_list():
    """
    !!! Не используется
    Возвращает на страницу результата поиска
    :return:
    """
    if ('psw' in session) and (session["psw"].strip() == ec_cfg.pswMarc) and (
            session["login"].strip() == ec_cfg.loginMarc):
        return render_template('tabResult.html', ls_book=session['find_ls_book'])
    return redirect(url_for('index'))


@app.route('/MarcWeb/getPdf', methods=['POST'])
@app.route('/getPdf', methods=['POST'])
def getPdf():
    """
    Выгрузка пользователю результата поиска в виде PDF файла
    через передачу списка с json и скрытой формы
    :return: PDF файл
    """
    hide_form = HideForm()
    ls_book = json.loads(hide_form.json_txt.data)
    fd, path = uploadPDF(ls_book)
    StartThreadDel(fd, path)
    return send_file(path)


if __name__ == '__main__':
    app.run(host=ec_cfg.host, port=ec_cfg.port)
