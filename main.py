from flask import Flask, render_template, request
import os
from LibMetod import *

app = Flask(__name__,  static_folder='static')
app.debug = True
# отключить кэш
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/')
def index():
    return render_template('authorize.html')

@app.route('/login', methods=['GET', 'POST'])
def authoriz():
    # if request.method == 'POST':
    return render_template('find.html')

@app.route('/find', methods=['POST'])
def find():
    if request.method == 'POST':
        # return render_template('tab_result.html')
        # print(type(request.form))
        # ls_book = parsFind(request.form)
        ls_book = crSpisBook(10)
        return render_template('tabResult.html', ls_book = ls_book)

@app.route('/book/<id>')
def infoBook(id):
    # return 'Book id: '+ str(id)
    return render_template('infoBook.html')


if __name__ == '__main__':
    app.run()