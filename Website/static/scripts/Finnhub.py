#!/usr/bin/env python
# coding: utf-8

# In[100]:

import finnhub
import datetime 


# In[101]:


key = "c6noq5iad3ibe15jd2e0"
stock_codes_list = ['AAPL', 'AMZN', 'GOOGL', 'TSLA', 'GME', 'SNAP', 'MRNA', 'BB', 'MANU', 'AAL']

finnhub_client = finnhub.Client(api_key=key)


# # Stocks

# In[117]:


def convertDateToUnix(day, month, year):
    """ Converting Date to Unix Time; return is an int """
    dt = datetime.datetime(year, month, day)
    timestamp = dt.replace(tzinfo=datetime.timezone.utc).timestamp()
    
    return int(timestamp)


def getStockPrice(stock_code, day, month, year): 
    """ This function returns the specified stock price @ a particular date """
    from_date = convertDateToUnix(day, month, year)  # converting date to unix - from
    to_date = from_date + 86400*7  # for utility purposes
    
    return finnhub_client.stock_candles(stock_code, 'D', from_date, to_date)['c'][0]


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


# In[118]:


#stock_prices = getAllStockPrices(stock_codes_list, 2, 12, 2021)
#print(stock_prices)


# # Crypto

# In[119]:


exchange_market = 'BINANCE:'
stable_coin = 'USDT'
crypto_codes_list = ['BTC', 'ADA']


def getCryptoPrice(crypto_code, day, month, year): 
    """ This function returns the specified crypto price @ a particular date """
    from_date = convertDateToUnix(day, month, year)  # converting date to unix - from
    to_date = from_date + 86400  # for utility purposes
    
    final_code = exchange_market+crypto_code+stable_coin
    
    return finnhub_client.crypto_candles(final_code, 'D', from_date, to_date)['c'][0]


def getAllCryptoPrices(crypto_codes, day, month, year):
    """ This function returns all predefined crypto prices as a 'Dict' """
    dict_crypto = {}
    for code in crypto_codes:
        dict_crypto[code] = getCryptoPrice(code, day, month, year)
    return dict_crypto


# In[120]:


#getAllCryptoPrices(crypto_codes_list, 8, 12, 2021)


# ## Crypto Demo
# 
# ### Calculating ROI

# In[125]:


""" function having 8 parameters: Coin, investment, 2 dates  """
pastVal = 1000
shares = calcNumOfShares(getCryptoPrice('ADA', 1, 12, 2021), pastVal)
currValue = calcCurrentValue(getCryptoPrice('ADA', 8, 12, 2021), shares)
roi_val, roi_perc = calcROI(currValue, pastVal)

#print(shares)
#print(currValue)
#print(getCryptoPrice('ADA', 1, 12, 2021))
#print(roi_val, roi_perc)

def __init__():
    #getAllCryptoPrices(crypto_codes_list, 8, 12, 2021)
    pass
