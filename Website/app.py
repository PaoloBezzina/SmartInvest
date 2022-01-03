from os import error
import os
import random
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
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

startAmount = 1000
interestRate = 0.001

def getRandomAmount():
    amount = random.randint(500, 5000)
    amount = round(amount/50)*50
    return amount

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
    subtractCurrentAssets()

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/assets'), 'smartInvestFavicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
    return redirect('/info.html')


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
    clearEvaluation();

    global dateString
    dateString, randDate = getRandomDate()
    initialiseFiles(randDate)

    setMoney(startAmount)

    return redirect('/dashboard.html')


@app.route('/simulate/', methods=['GET', 'POST'])
def addListing():
    if request.method == 'POST':
        code = request.form['code']
        amountInvested = request.form['amount-purchased']
        price = request.form['price']
        type = request.form['type']

        print(code)
        print(amountInvested)
        print(price)
        print(type)

        # get amount to subtract from wallet
        amountToSubtract = float(amountInvested)

        # get current wallet money
        walletAmount = float(getMoney())

        # if there is enough money remove money from wallet
        if walletAmount >= amountToSubtract:
            subtractMoney(amountToSubtract)
            addTransaction(code, amountInvested, price, type)

            #check if request came from /crypto.html or /stocks.html
            if type == "Stocks":
                # flash message to inform user of successful transaction after redirect
                flash('You have successfully purchased ' + amountInvested + ' shares of ' + code + ' at ' + price + ' per share.')
                return redirect('/stocks.html')
            else:
                flash('You have successfully purchased ' + amountInvested + ' shares of ' + code + ' at ' + price + ' per share.')
                return redirect('/crypto.html')

        else:
            flash(u"Not enough money", "error")
        
    else:
        print("error getting coin code")

    try:
        
        return ('', 204)
    except Exception as e:
        return str(e)


@app.route('/evaluate/', methods=['GET', 'POST'])
def evaluate():
    evaluation(getMoney(), startAmount, interestRate)
    try:
        return ('', 204)
    except Exception as e:
        return str(e)


@app.route("/get-money/", methods=['GET', 'POST'])
def getmoney():
    try:
        return (str(getMoney()))
    except Exception as e:
        return str(e)

def clearWalletListings():
    print("Clearing wallet listings")
    text_file = open("static/json/walletListings.json", "wt")
    text_file.write("[]")
    text_file.close()

def clearEvaluation():
    print("Clearing Evaluation")
    text_file = open("static/json/evaluation.json", "wt")
    text_file.write("[]")
    text_file.close()

    text_file = open("static/json/total_evaluation.json", "wt")
    text_file.write("[]")
    text_file.close()

# set main method
if __name__ == "__main__":
    app.run(debug=True)
