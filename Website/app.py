from os import error
import random
from flask import Flask, render_template, request, flash, redirect, url_for
from jinja2 import Template

# import local file Finnhub.py from subfolder scripts
from static.scripts.Finnhub import *

# To run just run: python -m flask run

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

global dateString
global randDate
start_date = datetime.date(2021, 1, 1)
end_date = datetime.date(2021, 12, 31)

def getRandomDate():
    global randDate
    global dateString

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    randDate = start_date + datetime.timedelta(days=random_number_of_days)
    dateString = randDate.strftime("%d/%m/%Y")

    print(dateString)
    print(randDate)

    return dateString, randDate

dateString, randDate = getRandomDate()


@app.before_first_request
def before_first_request():
    initialiseFiles(randDate)

@app.route('/')
def index():
    return redirect('/dashboard.html')


@app.route('/dashboard.html')
def load_dashboard():
    return render_template('dashboard.html', date=dateString)


@app.route('/crypto.html')
def load_crypto():
    return render_template('crypto.html')


@app.route('/stocks.html')
def load_stocks():
    return render_template('stocks.html')


@app.route('/info.html')
def load_info():
    return render_template('info.html')


@app.route('/restart')
def refreshEnvironment():
    clearWalletListings()
    global dateString
    dateString, randDate = getRandomDate()
    initialiseFiles(randDate)
    return redirect('/dashboard.html')


@app.route('/simulate/', methods=['GET', 'POST'])
def addListing():
    if request.method == 'POST':
        code = request.form['code']
        amount = request.form['amount-purchased']
        price = request.form['price']
        type = request.form['type']

        print(code)
        print(amount)
        print(price)
        print(type)

        addTransaction(code, amount, price, type)
    else:
        print("error getting coin code")

    try:
        return ('', 204)
    except Exception as e:
        return str(e)


@app.route('/evaluate/', methods=['GET', 'POST'])
def evaluate():
    evaluation(2000)
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


def clearWalletListings():
    print("Clearing wallet listings")
    text_file = open("static/json/walletListings.json", "wt")
    text_file.write("[]")
    text_file.close()


# set main method
if __name__ == "__main__":
    app.run(debug=True)
