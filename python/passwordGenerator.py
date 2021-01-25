import string
import random

#imports strings variables 
LETTERS = string.ascii_letters
NUMBERS = string.digits
PUNCTUATION = string.punctuation

#input for password lenght
def getPasswordLength():
    len = int(input("Type in the desired password lenght: "))
    return int(len)

#generator itself (default value set to 8)
def passwordGenerator(len=8):
    tempList = f'{LETTERS}{NUMBERS}{PUNCTUATION}'
    tempList = list(tempList)
    random.shuffle(tempList)

    randomPassword = random.choices(tempList, k=len)
    randomPassword = "".join(randomPassword)
    return randomPassword

passwordLenght = getPasswordLength()
defaultPassword = passwordGenerator()
randomPassword = passwordGenerator(passwordLenght)

print("Password ("+ str(len(defaultPassword)) + " digits):\t\t"+ defaultPassword)
print("Password ("+ str(len(randomPassword)) + " digits):\t\t"+ randomPassword)