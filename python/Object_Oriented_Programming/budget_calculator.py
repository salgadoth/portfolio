import os

class Budget(object):
    def __init__(self):
        os.system('cls')
        self.budget = float(input("How much is your budget?\n"))
        self.spending = self.budget * 0.5
        self.main()
    
    def main(self):
        os.system('cls')
        print("This calculator follows the 50-20-30 budget rule.\n")
        print("Your total budget is\n $", '{:.2f}'.format(self.budget))
        main_option = int(input("\n Choose an option:\n1- View overall budget \n2- View spending budget \n0- Quit.\n"))
        if main_option == 1:
            self.overall_budget()
        elif main_option == 2:
            self.spending_budget()
        else:
            quit()

    def overall_budget(self):
        os.system('cls')
        opt = int(input('How much do you want to save?\n1- 20% \n2- 30%')) 
        if opt == 1:
            self.saving = 0.2
        elif opt == 2:
            self.saving = 0.3
        else:
            print('\nERROR - Please choose between 1 or 2.')
        self.final_saving = self.budget * self.saving
        self.extra = self.budget - self.final_saving - self.spending
        print('\nSpending: $', '{:.2f}'.format(self.spending),'\nTo save: $', '{:.2f}'.format(self.final_saving), '\nExtra: $', '{:.2f}'.format(self.extra))
        os.system('pause')
        self.main()
    
    def spending_budget(self):
        os.system('cls')
        print('Spending Budget: $', '{:.2f}'.format(self.spending))
        rent = float(input('\nHow much rent do you pay monthly?\n'))
        bills = float(input('\nHow much are your monthly bills?\n'))
        groceries = self.spending - rent - bills
        print('\nExpenses: \nRent: $','{:.2f}'.format(rent),'\nBIlls: $','{:.2f}'.format(bills),'\nGroceries: $','{:.2f}'.format(groceries))
        os.system('pause')
        self.main()

Budget()