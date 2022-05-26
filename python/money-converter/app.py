import sys

moedas = {"REAL" : "real",
          "DOLAR" : "dolar",
          "EURO" : "euro"}

try:
    file = open("conversoes.bin", "rb")
    values = file.read(20)
except FileNotFoundError:
    print('Arquivo de configuração "conversoes.bin" não encontrado.')
    sys.exit(1)

file_moedas = []
moeda= ""
for bin_letter in values: 
    if bin_letter != 35:
        moeda += chr(bin_letter)
    else:
        for key, value in moedas.items():
            if value in moeda:
                file_moedas.append(key)
                moeda = ''
    
try:
    taxa = float(moeda)
except ValueError:
    print("Taxa de conversão incorreta, verifique arquivo .bin")
    sys.exit(1)

try:
    quantidade = float(input("Informe a quantidade de dinheiro à ser convertida: "))
except:
    print("Você não colocou um valor correto")
    sys.exit(1)
    
if quantidade < 0:
    print("Você não colocou um valor correto")
    sys.exit(1)
   
valor = taxa * quantidade

print("Você pagará {} {} por {} {}.".format(valor, file_moedas[0], quantidade, file_moedas[1]))
       

file.close()