import boto3
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from app.functions import *
import json 
import sys

ssm_client = boto3.client('ssm', region_name='sa-east-1')
response = ssm_client.get_parameter(Name='coinmarketcapAPI', WithDecryption=True)
coinmarketcapAPI = response["Parameter"]["Value"]

#constants
CURRENCY = 'USD'
LIMIT = 50
COUNTER = 0
SORT = 'market_cap'

while True:

	choice = input("Do you want to enter custom parameters?(Y/N): ").upper()
	if (choice == 'Y'):
		CURRENCY = input("What your local currency? (Default = USD) ").upper() 
		LIMIT = int(input("How many cryptocurrencies do you want to consult? (Default = 50) "))
		SORT = input("What do you want to sort by? (Default = Rank) ").lower()
		if (CURRENCY == '') or (LIMIT <= 0) or (SORT == ''):
			sys.exit("ERROR - INVALID PARAMETERS.")


	url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
	parameters = {
		'start' : '1',
		'limit' : LIMIT,
		'convert' : CURRENCY,
		'sort' : SORT,
	}

	headers = {
		'Accepts' : 'aplication/json',
		'X-CMC_PRO_API_KEY' : coinmarketcapAPI,
	}


	session = Session()
	session.headers.update(headers)

	try:
		response = session.get(url, params = parameters)
		results = response.json()
		data = results['data']
		#formatted_data = json.dumps(data, sort_keys=True, indent = 2)
		#print(results)
	except (ConnectionError, Timeout, TooManyRedirects) as e:
		print(e)



	for currency in data:
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
		COUNTER += 1
	
	runagain = input("Run Again?(Y/N): ").upper()
	if choice == "N":
		sys.exit("Ok. Exiting...")
