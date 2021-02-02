from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from app.functions import *
import json
import sys

CURRENCY = 'USD'

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

parameters = {
	'start' : '1',
	'convert' : CURRENCY,
}

headers = {
	'Accepts' : 'aplication/json',
	'X-CMC_PRO_API_KEY' : 'c13d9246-2806-4fc0-b8a2-3db224745082',
}


session = Session()
session.headers.update(headers)

try:
	response = session.get(url, params = parameters)
	results = response.json()
	data = results['data']
	#print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
	print(e)

pairs = {}

for currency in data:	
	symbol = currency['symbol']
	url = currency['id']
	pairs[symbol] = url

print(pairs)

while True:
	print()
	choice = input("Enter the symbol of a cryptocurrency: ").upper()

	for currency in data:
		if currency['symbol'] == choice:
			currencyQ = currency['quote'][CURRENCY]

			name = str(currency['name'])
			symbol = str(currency['symbol'])
			rank = currency['cmc_rank']
			price = currencyQ['price']
			last_updated = currencyQ['last_updated']
			market_cap = currencyQ['market_cap']
			percent_change_H = currencyQ['percent_change_1h']
			percent_change_D = currencyQ['percent_change_24h']
			percent_change_W = currencyQ['percent_change_7d']
			percent_change_M = currencyQ['percent_change_30d']

			rank_string = '{:,}'.format(rank)
			last_updated_string = last_updated[0:10] + " " + last_updated[11:-5]
			price_string = fstring(price, 3)
			market_cap_string = fstring(market_cap, 3)
			percent_change_H_string = fstring(percent_change_H, 2)
			percent_change_D_string = fstring(percent_change_D, 2)
			percent_change_W_string = fstring(percent_change_W, 2)
			percent_change_M_string = fstring(percent_change_M, 2)

			print()
			print("--------------------------------------------------------")
			print(
		  		"Name................: \t"+ name +
			  "\nSymbol..............: \t"+ symbol +
			  "\nRank................: \t"+ rank_string +
			  "\nPrice...............: \t"+ price_string +
			  "\nMarketCap...........: \t"+ market_cap_string +
			  "\nPercent Change Hour.: \t"+ percent_change_H_string + "%" +
			  "\nPercent Change Day..: \t"+ percent_change_D_string + "%" +
			  "\nPercent Change Week.: \t"+ percent_change_W_string + "%" +
			  "\nPercent Change Month: \t"+ percent_change_M_string + "%" +
			  "\nLast Update.........: \t"+ last_updated_string)
			print()
			print("--------------------------------------------------------")
		choice2 = input("Do you want to continue?(Y/N): ").upper()
		if choice2 == "N":
			sys.exit("Ok. Exiting...")