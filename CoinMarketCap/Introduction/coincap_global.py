import boto3
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects 
import json
from app.functions import *

ssm_client = boto3.client('ssm', region_name='sa-east-1')
response = ssm_client.get_parameter(Name='coinmarketcapAPI', WithDecryption=True)
coinmarketcapAPI = response["Parameter"]["Value"]

#constants
CURRENCY = 'USD'

choice = input("Do you want to enter custom parameters?(Y/N): ").upper()

if (choice == 'Y'):
	CURRENCY = input("What is your local currency? ").upper()

url = ' https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest'
parameters = {
	'convert': CURRENCY,
}

headers = {
	'Accepts' : 'aplication/json',
	'X-CMC_PRO_API_KEY' : coinmarketcapAPI,
}

session = Session()
session.headers.update(headers)

try:
	response = session.get(url, params = parameters)
	data = json.loads(response.text)
	formatted_data = json.dumps(data, sort_keys=True, indent=4)
	#print(formatted_data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
	print(e)

active_crypto = data['data']['active_cryptocurrencies']
btc_dominance = data['data']['btc_dominance']
eth_dominance = data['data']['eth_dominance']
total_mrkt_cap = data['data']['quote'][CURRENCY]['total_market_cap']
total_volume_24h = data['data']['quote'][CURRENCY]['total_volume_24h']

active_crypto_string = fstring(active_crypto, 3)
btc_dominance_string = fstring(btc_dominance, 2)
eth_dominance_string = fstring(eth_dominance, 2)
total_mrkt_cap_string = fstring(total_mrkt_cap, 3)
total_volume_24h_string = fstring(total_volume_24h, 3)


print()
print("Active Cryptocurrencies: " + active_crypto_string +
	  "\nBTC Dominance..........: " + btc_dominance_string + "%" +
	  "\nETC Dominance..........: " + eth_dominance_string + "%" +
	  "\nTotal MarketCap........: " + total_mrkt_cap_string +
	  "\nTotal Volume in 24Hr...: " + total_volume_24h_string)
print()


