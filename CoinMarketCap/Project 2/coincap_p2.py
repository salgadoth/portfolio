#Lib's or modules used
import os
import boto3
import json
import time
from app.functions import *
from requests import Session, Request
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

#GETTING API PARAMS FROM AWS SYSTEM MANAGER THROUGH BOTO3'S SSM CLIENT
ssm_client = boto3.client('ssm', region_name='sa-east-1')
response = ssm_client.get_parameter(Name='coinmarketcapAPI', WithDecryption = True)
coinmarketcapAPI = response["Parameter"]["Value"]

#SETTING GLOBAL CONSTANTS AND PARAMETERS
CONVERT = input("What is your local currency? ").upper()
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
	print("OK...")
	pass
else:
	print()
	print("WRONG OPTION...")

session = Session()
session.headers.update(HEADERS)

#CONNECTING TO API AND STORING DATA IN ARRAY
try: 
	response = session.get(GLOBAL_URL, params = PARAMETERS)
	results = response.json()
	#print(results)
	data = results['data']
except (ConnectionError, Timeout, TooManyRedirects) as e:
	print(e)

print()
print("ALERTS TRACKING...")
print()

#SET A ALREADY HIT ARRAY
already_hit = []

while True:
	#READS ALERT
	with open("alerts.txt") as inp:
		for line in inp:
			crypto, target = line.split() 
			
			for currency in data:
				if currency['symbol'] == crypto:
					quotes = currency['quote'][CONVERT]

					name = str(currency['name'])
					symbol = str(currency['symbol'])
					price = quotes['price']
					last_updated = quotes['last_updated']

					last_updated_string = last_updated[0:10] + " " + last_updated[11:-5]

					if float(price) >= float(target) and symbol not in already_hit:
						print(name + " hit " + target + " on " + last_updated_string)
						already_hit.append(symbol)
	time.sleep(300)
	print("......")
