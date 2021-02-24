from flask import Flask, render_template, request, session
import os
from LibMetod import *

app = Flask(__name__,  static_folder='static')
app.debug = True
app.config['SECRET_KEY'] = '38899ebc4e1575cc5199d9268611741bb7569903'
# отключить кэш
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
        # print(ls_id)
        marc = Class_Sql()
        ls_book = marc.getSpisBook(ls_id)
        if ('psw' in session) and (session["psw"].strip() == '1'):
            return render_template('tabResult.html', ls_book = ls_book)
        else:
            return render_template('authorize.html')


@app.route('/book/<id>')
def infoBook(id):
    if ('psw' in session) and (session["psw"].strip() == '1'):
        print('Book_Id: ', id)
        ls_tag = getInfoBook(id)
        return render_template('infoBook.html', ls_tag = ls_tag)
    else:
        return render_template('authorize.html')


if __name__ == '__main__':
    app.run()