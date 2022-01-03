#!/usr/bin/env python
# coding: utf-8

import json
import finnhub
from datetime import date
import datetime
from currency_converter import CurrencyConverter


key = "c6noq5iad3ibe15jd2e0"
stock_codes_list = ['AAPL', 'AMZN', 'GOOGL', 'TSLA',
                    'GME', 'SNAP', 'MRNA', 'BB', 'MANU', 'AAL', 'STNE', 'GOCO', 'PSFE', 'PTON']
stock_names_list = ["Apple", "Amazon", "Google", "Tesla", "Gamestop", "Snapchat", "Moderna",
                    "BlackBerry", "Manchester United", "American Airlines", "StoneCo Ltd.", "GoHealth Inc.", "Paysafe Ltd.", "Peloton Interactive Inc."]

finnhub_client = finnhub.Client(api_key=key)  # FinnHub Crypto/Stocks API


# # Stocks

def convertDateToUnix(day, month, year):
    """ Converting Date to Unix Time; return is an int """
    dt = datetime.datetime(year, month, day)
    timestamp = dt.replace(tzinfo=datetime.timezone.utc).timestamp()

    return int(timestamp)


def getStockPrice(stock_code, day, month, year):
    """ This function returns the specified stock price @ a particular date """

    c = CurrencyConverter()  # currency convertor API

    # converting date to unix - from
    to_date = convertDateToUnix(day, month, year)
    from_date = to_date - 86400*7  # for utility purposes

    price = finnhub_client.stock_candles(
        stock_code, 'D', from_date, to_date)['c'][-1]
    return round(c.convert(price, 'USD', 'EUR'), 2)


def getAllStockPrices(stock_codes, day, month, year):
    """ This function returns all predefined stock prices as a 'Dict' """
    dict_stocks = {}
    for code in stock_codes:
        dict_stocks[code] = getStockPrice(code, day, month, year)
    return dict_stocks


def calcNumOfShares(price, amount):
    """ This function calculate the number of shares invested """
    return amount/price


def calcCurrentValue(price, shares):
    """ This function calculates the current value of investment """
    return price*shares


def calcROI(currentValue, pastValue):
    """ This function calculates the ROI as a value and as a % """
    roi_value = currentValue - pastValue
    roi_perc = (roi_value/pastValue)*100

    return roi_value, roi_perc


def convertStocksToJSON(stock_codes, stock_names, day, month, year):
    """ This function writes a JSON file that will be used to populate the web page """
    stock_prices = getAllStockPrices(stock_codes, day, month, year)

    json = []
    for (key, value, name) in zip(stock_prices.keys(), stock_prices.values(), stock_names):
        temp_dict = {}
        temp_dict["code"] = key
        temp_dict["title"] = name
        temp_dict["value"] = value
        temp_dict["href"] = "/simulate"
        temp_dict["info"] = "https://finance.yahoo.com/quote/"+key+"/"
        json.append(temp_dict)

    json_str = str(json)

    text_file = open("static/json/stocksListings.json", "wt")
    json_str = json_str.replace("'", '"')
    n = text_file.write(json_str)
    text_file.close()


exchange_market = 'BINANCE:'
stable_coin = 'USDT'
crypto_codes_list = ['BTC', 'ETH', 'ADA', 'LTC',
                     'XRP', 'ZRX', 'XLM', 'SOL', 'DOGE', 'LINK']
crypto_names_list = ['Bitcoin', 'Ether', 'Cardano', 'Litecoin',
                     'Ripple', '0x', 'Stellar', 'Solana', 'DogeCoin', 'Chainlink']


def getCryptoPrice(crypto_code, day, month, year):
    """ This function returns the specified crypto price @ a particular date """

    c = CurrencyConverter()  # currency convertor API

    # converting date to unix - from
    from_date = convertDateToUnix(day, month, year)
    to_date = from_date + 86400  # for utility purposes

    final_code = exchange_market+crypto_code+stable_coin

    price = finnhub_client.crypto_candles(
        final_code, 'D', from_date, to_date)['c'][0]
    return round(c.convert(price, 'USD', 'EUR'), 2)


def getAllCryptoPrices(crypto_codes, day, month, year):
    """ This function returns all predefined crypto prices as a 'Dict' """
    dict_crypto = {}
    for code in crypto_codes:
        dict_crypto[code] = getCryptoPrice(code, day, month, year)
    return dict_crypto


def convertCryptoToJSON(crypto_codes, crypto_names, day, month, year):
    """ This function writes a JSON file that will be used to populate the web page """
    crypto_prices = getAllCryptoPrices(crypto_codes, day, month, year)

    crypto_webpage_url = "https://coinmarketcap.com/currencies/"

    json = []
    for (key, value, name) in zip(crypto_prices.keys(), crypto_prices.values(), crypto_names):
        temp_dict = {}
        temp_dict["code"] = key
        temp_dict["title"] = name
        temp_dict["value"] = value
        temp_dict["href"] = "/simulate"
        temp_dict["info"] = crypto_webpage_url+name+"/"
        json.append(temp_dict)

    json_str = str(json)

    text_file = open("static/json/cryptoListings.json", "wt")
    json_str = json_str.replace("'", '"')
    n = text_file.write(json_str)
    text_file.close()

    """ function having 8 parameters: Coin, investment, 2 dates  """


def addTransaction(code, amount, price, type_name, stock_names=stock_names_list, stock_codes=stock_codes_list, crypto_names=crypto_names_list, crypto_codes=crypto_codes_list):
    """ This function will add the transaction to our wallet """

    name = ""
    if type_name == 'Stocks':
        name = stock_names[stock_codes.index(code)]
    else:
        name = crypto_names[crypto_codes.index(code)]

    with open('static/json/walletListings.json') as f:
        data = json.load(f)

    price = float(price)
    amount = float(amount)

    temp_dict = {}
    temp_dict['code'] = code
    temp_dict['title'] = name
    temp_dict['price'] = price
    temp_dict['units'] = calcNumOfShares(price, amount)
    temp_dict['value'] = amount
    temp_dict['type'] = type_name

    data.append(temp_dict)

    data_str = str(data)

    text_file = open("static/json/walletListings.json", "wt")
    data_str = data_str.replace("'", '"')
    n = text_file.write(data_str)
    text_file.close()


def evaluation(wallet_amount, total_past_value, interestRate):
    """ This function is used to give the final evaluation on the ROI from the transaction/s """

    with open('static/json/walletListings.json') as f:
        data = json.load(f)

    total_past_value_amount = total_past_value
    total_current_value_amount = wallet_amount
    evaluation_list = []
    for transaction in data:
        temp_dict = {}

        pastVal = transaction['value']

        today = str(date.today()).split('-')
        day = int(today[2])
        month = int(today[1])
        year = int(today[0])

        if transaction['type'] == 'Stocks':
            current_price = getStockPrice(
                transaction['code'], day, month, year)
        else:
            current_price = getCryptoPrice(
                transaction['code'], day, month, year)

        currVal = calcCurrentValue(current_price, transaction['units'])
        total_current_value_amount += currVal

        roi_val, roi_perc = calcROI(currVal, pastVal)

        temp_dict['code'] = transaction['code']
        temp_dict['pastValue'] = transaction['value']
        temp_dict['currentValue'] = currVal
        temp_dict['pastPrice'] = transaction['price']
        temp_dict['currentPrice'] = current_price
        temp_dict['roiVal'] = roi_val
        temp_dict['roiPerc'] = roi_perc

        evaluation_list.append(temp_dict)

    # adding interest to the wallet
    total_current_value_amount += (wallet_amount * interestRate)
    interestDict = {'code': "Bank interest", 'pastValue': wallet_amount,
                    'currentValue': (wallet_amount + (wallet_amount * interestRate)), 'pastPrice': '', 'currentPrice': '', 'roiVal': (wallet_amount * interestRate), 'roiPerc': interestRate*100}
    evaluation_list.append(interestDict)

    total_roi_val, total_roi_perc = calcROI(
        total_current_value_amount, total_past_value_amount)
    total_dict = {'pastValue': total_past_value_amount, 'currentValue': total_current_value_amount,
                  'totalROIVal': total_roi_val, 'totalROIPerc': total_roi_perc}

    evaluation_str = str(evaluation_list)
    text_file = open("static/json/evaluation.json", "wt")
    evaluation_str = evaluation_str.replace("'", '"')
    n = text_file.write(evaluation_str)
    text_file.close()

    total_evaluation_str = str(total_dict)
    text_file = open("static/json/total_evaluation.json", "wt")
    total_evaluation_str = total_evaluation_str.replace("'", '"')
    n = text_file.write(total_evaluation_str)
    text_file.close()


def initialiseFiles(date):
    year, month, day = str(date).split('-')
    day = int(day)
    month = int(month)
    year = int(year)

    convertCryptoToJSON(crypto_codes_list, crypto_names_list, day, month, year)
    convertStocksToJSON(stock_codes_list, stock_names_list, day, month, year)


global amountInWallet
amountInWallet = 1000


def getMoney():
    return amountInWallet


def setMoney(amount):
    global amountInWallet
    amountInWallet = amount


def subtractMoney(amount):
    global amountInWallet
    amountInWallet -= amount
    return amountInWallet


def subtractCurrentAssets():
    # read data from json file
    with open('static/json/walletListings.json') as f:
        data = json.load(f)

        # if data is empty, return
        if len(data) == 0:
            return
        else:
            # subtract current assets
            for transaction in data:

                amount = transaction['value']
                subtractMoney(amount)


def __init__():
    pass
