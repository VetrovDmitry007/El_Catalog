from flask import Flask, render_template, session, send_file, request
from App.LibMetod import *
from App import ec_cfg

app = Flask(__name__, static_folder='static')
app.debug = ec_cfg.debugFlask
app.config['SECRET_KEY'] = ec_cfg.SECRET_KEY
# отключить кэш CSS
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/MarcWeb/Work.asp')
@app.route('/')
def index():
    return render_template('authorize.html')


@app.route('/MarcWeb/exit')
@app.route('/exit')
def session_exit():
    session.pop('psw')
    session.pop('login')
    return render_template('authorize.html')


@app.route('/MarcWeb/login', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def authoriz():
    """
    Форма авторизации ползователя
    :return: Форма поиска
    """
    if request.method == 'POST':
        session['psw'] = request.form['password']
        session['login'] = request.form['login']
    if ('psw' in session) and (session["psw"].strip() == ec_cfg.pswMarc) and (
            session["login"].strip() == ec_cfg.loginMarc):
        return render_template('find.html')
    else:
        return render_template('authorize.html')


@app.route('/MarcWeb/find', methods=['POST'])
@app.route('/find', methods=['POST'])
def find():
    """
    Возвращает список найденной литературы
    :return: Список словарей
    """
    if request.method == 'POST':
        if ('psw' in session) and (session["psw"].strip() == ec_cfg.pswMarc) and (
                session["login"].strip() == ec_cfg.loginMarc):
            ls_id = findBook(request.form)
            marc = Class_Sql()
            ls_book = marc.getSpisBook(ls_id)
            session.pop('find_ls_book')
            session['find_ls_book'] = ls_book
            return render_template('tabResult.html', ls_book=ls_book)
        else:
            return render_template('authorize.html')


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
        return render_template('infoBook.html', ls_tag=ls_tag, book_id=id)
    else:
        return render_template('authorize.html')


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
    else:  # если файл макрообъекта не создан
        return render_template('find.html')


@app.route('/MarcWeb/result_find')
@app.route('/result_find')
def return_list():
    """
    Возвращает на страницу результата поиска
    :return:
    """
    if ('psw' in session) and (session["psw"].strip() == ec_cfg.pswMarc) and (
            session["login"].strip() == ec_cfg.loginMarc):
        return render_template('tabResult.html', ls_book=session['find_ls_book'])
    return render_template('authorize.html')


@app.route('/MarcWeb/getPdf')
@app.route('/getPdf')
def getPdf():
    """
    Выгрузка пользователю результата поиска в виде PDF файла
    через передачу списка с пом. сессии
    :return: PDF файл
    """
    fd, path = uploadPDF(session['find_ls_book'])
    StartThreadDel(fd, path)
    return send_file(path)


if __name__ == '__main__':
    app.run(host=ec_cfg.host, port=ec_cfg.port)
