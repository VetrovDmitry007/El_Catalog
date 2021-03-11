from flask import Flask, render_template, session, send_file, request
from App.LibMetod import *
from App import ec_cfg
from App.Forms import LoginForm, FindForm

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
    login_form = LoginForm()
    session.pop('psw')
    session.pop('login')
    # login_form.username.data = ''
    # login_form.password.gettext('')
    return render_template('authorize.html', form=login_form)


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
    return render_template('authorize.html', form=login_form)


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
    find_form = FindForm()
    ls_id = findBook(find_form)
    marc = Class_Sql()
    ls_book = marc.getSpisBook(ls_id)
    if ('psw' in session) and (session["psw"].strip() == ec_cfg.pswMarc) and (
            session["login"].strip() == ec_cfg.loginMarc):
        fd, path = uploadPDF(ls_book)
        StartThreadDel(fd, path)
        return render_template('tabResult.html', ls_book=ls_book, patch_pdf=path)
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
    # если файл макрообъекта не создан
    return render_template('find.html')


@app.route('/MarcWeb/export/<patch_pdf>')
@app.route('/export/<patch_pdf>')
def getPdf(patch_pdf):
    """
    Выгрузка пользователю результата поиска в виде PDF файла
    :param patch_pdf: Путь к временному PDF файлу
    :return: PDF файл
    """
    return send_file(patch_pdf)


if __name__ == '__main__':
    app.run(host=ec_cfg.host, port=ec_cfg.port)
