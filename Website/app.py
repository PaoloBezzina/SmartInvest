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

startAmount = 5000

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
    setMoney(startAmount)
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
    print("test")
    global dateString
    dateString, randDate = getRandomDate()
    initialiseFiles(randDate)
    setMoney(startAmount)
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


@app.route("/get-money/", methods=['GET', 'POST'])
def getmoney():

    print(getMoney())

    try:
        return ('', 204)
    except Exception as e:
        return str(e)


@app.route("/subtract-money/", methods=['GET', 'POST'])
def subtractmoney():
    print("Subtracting money")

    # get amount to subtract
    if request.method == 'POST':
        amount = request.form['amount']
        amount = int(amount)

    # get current wallet money
    wallet = int(getMoney())

    # if there is enough money remove money from wallet
    if wallet >= amount:
        subtractMoney(amount)
        print("Subtracted " + str(amount) + " from wallet")
        print("New amount " + str(getMoney()) + " in wallet")
    else:
        print("Not enough money")

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
