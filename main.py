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

@app.route('/login', methods=['POST'])
def authoriz():
    if request.method == 'POST':
        return render_template('find.html')

@app.route('/find', methods=['POST'])
def find():
    if request.method == 'POST':
        # return render_template('tab_result.html')
        # print(type(request.form))
        # print(request.form)
        print(f1(request.form))
        return render_template('tabResult.html')


if __name__ == '__main__':
    app.run()