class SoapBarSale():
    """
    Class for soap bar sales

    Args:
        Sales (class): processes data
    """
    def __init__(self, amount) -> None:
        self.gross = 10
        self.amount = 1
        self.net = 10*0.75
        self.tax = 10*0.25
        self.amount = amount
class LiquidSoapSale():
    """
    Class for soap bar sales

    Args:
        Sales (class): processes data
    """
    def __init__(self, amount) -> None:
        self.gross = 10
        self.amount = 1
        self.net = 10*0.75
        self.tax = 10*0.25
        self.amount = amount
class CoconutOilSale():
    """
    Class for soap bar sales

    Args:
        Sales (class): processes data
    """
    def __init__(self, amount) -> None:
        self.gross = 10
        self.amount = 1
        self.net = 10*0.75
        self.tax = 10*0.25
        self.amount = amount
class LuteSale():
    """
    Class for soap bar sales

    Args:
        Sales (class): processes data
    """
    def __init__(self, amount) -> None:
        self.gross = 10
        self.amount = 1
        self.net = 10*0.75
        self.tax = 10*0.25
        self.amount = amount

def product_menu():
    """
    prints products and based on choise calls a parent
    """
    print(
        """
        ---Products---
        1. Soap Bar
        2. Liquid Soap
        3. Coconut Oil
        4. NaOH
        """
        )
    while True:
        choise = input("Choose an option: \n")
        if choise == '1':
            bars = input("How many soap bars?\n")
            print(f"Got it. {bars} bars of soap")
            return [1, bars]
        if choise == '2':
            bottles = input("How many bottles")
            print(f"Got it. {bottles} bottles of soap")
            return [2, bottles]
        if choise == '3':
            jars = input("How many jars?\n")
            print(f"Got it. {jars} jars of coconut oil")
            return [3, jars]
        if choise == '4':
            cans = input("How many cans?\n")
            print(f"Got it. {cans} cans of lute")
            return [4, cans]
        print("Not a valid input please enter a number 1-4")

class Sales(SoapBarSale, LiquidSoapSale, CoconutOilSale, LuteSale):
    """
    Class for recording a transaction
    """
    def __init__(self) -> None:
        self.post = []
        self.product = product_menu()
        if self.product[1] == 1:
            SoapBarSale.__init__(self, self.product[2])
        if self.product[1] == 2:
            LiquidSoapSale.__init__(self, self.product[2])
        if self.product[1] == 3:
            CoconutOilSale.__init__(self, self.product[2])
        if self.product[1] == 4:
            LuteSale.__init__(self, self.product[2])
    def credit_sale(self) -> None:
        """
        Credit sale method - changes GL accounts accordingly
        """
        self.post = ['Trade Receivables', 'Current Assets']
    def cash_sale(self) -> None:
        """
        Cash sale method - changes GL accounts accordingly
        """
        self.post = ['Sales', 'Sales Tax', 'Current Assets']
