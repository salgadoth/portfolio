#Lib's used

import os
import json
import boto3
from app.functions.functions import *
from requests import Session, Request 
from prettytable import PrettyTable
from colorama import Fore, Back, Style
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects 

#GETTING API PARAM FROM AWS SYSTEM MANAGER THROUGH BOTO3'S SSM CLIENT 
ssm_client = boto3.client('ssm', region_name='sa-east-1')
response = ssm_client.get_parameter(Name='coinmarketcapAPI', WithDecryption=True)
coinmarketcapAPI = response["Parameter"]["Value"]

#SETTING GLOBAL CONSTANTS AND PARAMETERS
CONVERT = input('What is your local currency? ').upper()
GLOBAL_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
PARAMETERS = {
	'start' : '1',
	'convert' : CONVERT,
}
HEADERS = {
	'Accepts' : 'application/json',
	'X-CMC_PRO_API_KEY' : coinmarketcapAPI,
}

choice = input("Do you want to update your portfolio (Y/N)? ").upper()
if choice == "Y":
	addcrypto()
elif choice == "N":
	print()
	print("Ok...")
	pass
else:
	print("Wrong option.")

session = Session()
session.headers.update(HEADERS)

try: 
	response = session.get(GLOBAL_URL, params = PARAMETERS)
	results = response.json()
	data = results['data']
except (ConnectionError, Timeout, TooManyRedirects) as e:
	print(e)
 

pairs = {}
for currency in data:
	symbol = currency['symbol']
	cryptoID = currency['id']
	pairs[symbol] = cryptoID

print()
print("MY PORTFOLIO")
print()

portfolio_value = 0.00
last_updated = 0

table = PrettyTable(['Asset', 'Amount Owned', CONVERT + " value", "Price", "1H", "24H", "7D"])

with open("portfolio.txt") as inp:
	for line in inp:
		crypto, amount = line.split()
		crypto = crypto.upper()

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

		value_string = fstring(value, 2)
		price_string = fstring(price, 2)

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
print("Total portfolio value: " + Back.GREEN + "$" + portfolio_value_string + Style.RESET_ALL)
print()
print("Last updated: " + last_updated_string)	