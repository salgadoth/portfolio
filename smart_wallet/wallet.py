import json
import time
import ccxt
import boto3
from prettytable import PrettyTable
from colorama import Fore, Back, Style
from binance.client import Client
from requests import Session, Request
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from app.functions.functions import *

ssm_client = boto3.client("ssm", region_name='sa-east-1')
response = ssm_client.get_parameter(Name = "Binance_API_Key", WithDecryption = True)
BINANCE_API = response["Parameter"]["Value"]
response = ssm_client.get_parameter(Name = "Binance_Secret_API_Key", WithDecryption = True)
BINANCE_API_SECRET = response["Parameter"]["Value"]
response = ssm_client.get_parameter(Name = 'coinmarketcapAPI', WithDecryption = True)
CMC_API = response['Parameter']['Value']

CONVERT = input("What is your local currency? ").upper()
GLOBAL_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
PARAMETERS = {
    'start' : '1',
    'convert' : CONVERT,
}
HEADERS = {
    'Accepts' : 'application/json',
    'X-CMC_PRO_API_KEY': CMC_API,
}

binance = ccxt.binance({
    'options': {
        'adjustForTimeDifference': True,
    },
    'apiKey': BINANCE_API,
    'secret': BINANCE_API_SECRET,
})

binData = binance.fetch_balance()
balances = binData['info']['balances']
portfolio = {}
for asset in balances:
   if float(asset['free']) > 0:
       crypto = asset['asset']
       amount =  asset['free']
       portfolio[crypto] = amount
#print(portfolio)


session = Session()
session.headers.update(HEADERS)

while True:
    try:
        response = session.get(GLOBAL_URL, params = PARAMETERS)
        results = response.json()
        data = results['data']
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    print()
    print('\t\t\t\t\t\tMY PORTFOLIO')
    print()

    portfolio_value = 0
    last_updated = 0

    table = PrettyTable(['Asset', 'Amount Owned', CONVERT + ' value', 'Price', '1H', '24H', '7D'])

    for crypto in portfolio:
        amount = portfolio[crypto]
        for currency in data:
            if currency['symbol'] == crypto:
                quotes = currency['quote'][CONVERT]
                
                name = str(currency['name'])
                symbol = str(currency['symbol'])
                rank = currency['cmc_rank']
                price = quotes['price']
                last_updated = quotes['last_updated']
                hour_change = quotes['percent_change_1h']
                daily_change = quotes['percent_change_24h']
                weekly_change = quotes['percent_change_7d']

                value = float(price) * float(amount)
                
                #print(value)
                #print(currency['symbol'], amount)

        if hour_change > 0:
            hour_color = Back.GREEN + str(hour_change) + '%' + Style.RESET_ALL
        else:
            hour_color = Back.RED + str(hour_change) + '%' + Style.RESET_ALL

        if daily_change > 0:
            daily_color = Back.GREEN + str(daily_change) + '%' + Style.RESET_ALL
        else:
            daily_color = Back.RED + str(daily_change) + '%' + Style.RESET_ALL

        if weekly_change > 0:
            weekly_color = Back.GREEN + str(weekly_change) + '%' + Style.RESET_ALL
        else:
            weekly_color = Back.RED + str(weekly_change) + '%' + Style.RESET_ALL

        portfolio_value += value
        #print(portfolio_value)

        value_string = fstring(value, 2)
        price_string = fstring(price, 2)
        #print(value_string)

        table.add_row([name + ' (' + symbol + ') ',
                            amount,
                            '$' + value_string,
                            '$' + price_string,
                            str(hour_color),
                            str(daily_color),
                            str(weekly_color)])

    print(table)
    print()

    portfolio_value_string = fstring(portfolio_value, 2)
    last_updated_string = last_updated[0:10] + " " + last_updated[11:-5]
    print("Total portfolio value: " + Back.GREEN + '$' + portfolio_value_string + Style.RESET_ALL)
    print()
    print("Last updated: " + last_updated_string)

    time.sleep(60)
