from os import error
from flask import Flask, render_template, request, flash, redirect, url_for
from jinja2 import Template

#import local file Finnhub.py from subfolder scripts
from static.scripts.Finnhub import *

# To run just run: python -m flask run

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
crypto_codes_list = ['BTC', 'ADA']

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/dashboard.html')
def load_dashboard():
    return render_template('dashboard.html')

@app.route('/crypto.html')
def load_crypto():
    return render_template('crypto.html')

@app.route('/stocks.html')
def load_stocks():
    return render_template('stocks.html')

@app.route('/info.html')
def load_info():
    return render_template('info.html')

@app.route('/simulate/', methods=['GET', 'POST'])
def get_Crypto_Code():
    if request.method == 'POST':
        print("coin-code")
        coin_code = request.form['coin-code']
        print(coin_code)
    else:
        print("error getting coin code")

    try:
        return ('', 204)
    except Exception as e:
        return str(e)

@app.route("/get-bitcoin/", methods=['GET', 'POST'])
def process_file():

    #prices = getAllCryptoPrices(['BTC'], 8, 12, 2021)

    try:
        return ('', 204)
    except Exception as e:
        return str(e)

#set main method
if __name__ == "__main__":
    app.run(debug=True)
