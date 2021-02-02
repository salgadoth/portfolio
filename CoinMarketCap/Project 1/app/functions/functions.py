def fstring(arg1, arg2):
	formatted_string = '{:,}'.format(round(arg1, arg2))
	return formatted_string

def addcrypto():
	f = open("portfolio.txt", "a")
	f.write("\n" + (input("Type in your cryptocurrencies (SYMBOL:AMOUNT): ").upper()))
	f.close