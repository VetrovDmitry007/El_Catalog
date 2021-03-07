from flask import Flask, render_template, session, send_file
from LibMetod import *

app = Flask(__name__,  static_folder='static')
app.debug = True
app.config['SECRET_KEY'] = '38899ebc4e1575cc5199d9268611741bb7569903'
# отключить кэш CSS
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/')
def index():
    return render_template('authorize.html')

@app.route('/exit')
def session_exit():
    session.pop('psw')
    return render_template('authorize.html')

@app.route('/login', methods=['GET', 'POST'])
def authoriz():
    if request.method == 'POST':
        session['psw'] = request.form['password']
    if ('psw' in session) and (session["psw"].strip() == '1'):
        return render_template('find.html')
    else:
        return render_template('authorize.html')


@app.route('/find', methods=['POST'])
def find():
    if request.method == 'POST':
        ls_id = findBook(request.form)
        marc = Class_Sql()
        ls_book = marc.getSpisBook(ls_id)
        # print(ls_book)
        if ('psw' in session) and (session["psw"].strip() == '1'):
            return render_template('tabResult.html', ls_book = ls_book)
        else:
            return render_template('authorize.html')


@app.route('/export/<ls>')
def getPdf(ls):

    return ls

@app.route('/book/<id>')
def infoBook(id):
    if ('psw' in session) and (session["psw"].strip() == '1'):
        ls_tag = getInfoBook(id)
        print(ls_tag)
        return render_template('infoBook.html', ls_tag = ls_tag, book_id = id)
    else:
        return render_template('authorize.html')

@app.route('/upload/<book_id>')
def upload_file(book_id):
    tpl = uploadFile(book_id)  # кортэж (fd, path)
    if tpl:
        fd, path = tpl
        StartThreadDel(fd, path)
        return send_file(path) # посмотреть справку по send_file()
    else:  # если файл макрообъекта не создан
        return render_template('find.html')


@app.route('/export_tmp/<ls_books>')
def export_pdf(ls_books):
    tpl = uploadPDF(ls_books)  # кортэж (fd, path)
    if tpl:
        fd, path = tpl
        StartThreadDel(fd, path)
        return send_file(path)
    else:  # если файл не создан
        return render_template('find.html')


if __name__ == '__main__':
    app.run()