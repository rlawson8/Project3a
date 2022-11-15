'''
This web service extends the Alphavantage api by creating a visualization module, 
converting json query results retuned from the api into charts and other graphics. 

This is where you should add your code to function query the api
'''
from asyncio.log import logger
from cmath import log
import requests
from datetime import datetime
from datetime import date
import pygal


#Helper function for converting date
def convert_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d')

def call_ap(chartType, stockSymbol, startDate_dt, endDate_dt, time_series):
    dateKeyList = []
    openValues = []
    highValues = []
    lowValues = []
    closeValues = []

    if chartType == "1":
        chart = pygal.Bar()
    else:
        chart = pygal.Line()
    chart.title = 'Stock Data for ' + stockSymbol + ': ' + str(startDate_dt.date()) + ' to ' + str(endDate_dt.date())
    if time_series == "1":
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+stockSymbol+'&interval=60min&outputsize=full&apikey=TF2MH4AQ3EMH4GZL'
    elif time_series == "2":
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol='+stockSymbol+'&outputsize=full&apikey=TF2MH4AQ3EMH4GZL'
    elif time_series == "3":
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol='+stockSymbol+'&outputsize=full&apikey=TF2MH4AQ3EMH4GZL'
    else:
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol='+stockSymbol+'&outputsize=full&apikey=TF2MH4AQ3EMH4GZL'
    r = requests.get(url)
    data = r.json()
    data.pop('Meta Data')
    dateList = data.values()
    for dictionary in dateList:
        for dateKey in dictionary:
            if time_series == "1":
                dateKey_dt = datetime.strptime(dateKey, "%Y-%m-%d %H:%M:%S")
            else:
                dateKey_dt = datetime.strptime(dateKey, "%Y-%m-%d")

            if startDate_dt <= dateKey_dt <= endDate_dt:  
                dateKeyList.append(dateKey)
                openValues.append(float(dictionary[dateKey]['1. open']))
                highValues.append(float(dictionary[dateKey]['2. high']))
                lowValues.append(float(dictionary[dateKey]['3. low']))
                closeValues.append(float(dictionary[dateKey]['4. close']))
    dateKeyList.reverse()
    openValues.reverse()
    highValues.reverse()
    lowValues.reverse()
    closeValues.reverse()
    chart.x_labels = map(str, dateKeyList)
    chart.add('Open', openValues)
    chart.add('High', highValues)
    chart.add('Low', lowValues)
    chart.add('Close', closeValues)
    return chart.render_data_uri()
