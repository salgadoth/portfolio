def addcrypto():
	f = open("alerts.txt", "a")
	f.write("\n" + (input("Type in your cryptocurrencies (SYMBOL TARGET_PRICE:").upper()))
	f.close