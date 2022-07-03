from run import ACCOUNTS, GENERAL_LEDGER, RECEIVABLES, choose_customer, append_data

class SoapBarSale():
    """
    Class for soap bar sales

    Args:
        Sales (class): processes data
    """
    def __init__(self, amount) -> None:
        self.gross = 10*amount
        self.amount = 1
        self.net = self.gross*0.75
        self.tax = self.gross*0.25
        self.amount = amount
        
class LiquidSoapSale():
    """
    Class for soap bar sales

    Args:
        Sales (class): processes data
    """
    def __init__(self, amount) -> None:
        self.gross = 10*amount
        self.amount = 1
        self.net = self.gross*0.75
        self.tax = self.gross*0.25
        self.amount = amount
class CoconutOilSale():
    """
    Class for soap bar sales

    Args:
        Sales (class): processes data
    """
    def __init__(self, amount) -> None:
        self.gross = 10*amount
        self.amount = 1
        self.net = self.gross*0.75
        self.tax = self.gross*0.25
        self.amount = amount
class LuteSale():
    """
    Class for soap bar sales

    Args:
        Sales (class): processes data
    """
    def __init__(self, amount) -> None:
        self.gross = 10*amount
        self.amount = 1
        self.net = self.gross*0.75
        self.tax = self.gross*0.25
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
        self.customer = choose_customer()
        self.date = None
        self.type = None
        self.trans_id = None
        self.inv_no = None
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
        Credit sale method - changes type to 1
        """
        self.type = 1
        choose_customer()
    def cash_sale(self) -> None:
        """
        Cash sale method - changes type to 2
        """
        self.type = 2
    def write_transaction(self):
        """
        Writes transaction to accounts
        """
        if self.type == 1:
            append_data(
                GENERAL_LEDGER, 'Trade Receivables', [self.customer, self.trans_id, self.gross]
                )
            append_data(
                GENERAL_LEDGER, 'Current Assets', ['', '', '', self.customer, self.trans_id, self.gross]
                )
            append_data(
                RECEIVABLES, self.customer, ['Invoice', self.gross, self.inv_no]
                )
            append_data(
                ACCOUNTS, 'sdb', [self.date, self.customer, self.net, self.tax, self.gross]
                )
        if self.type == 2:
            append_data(
                GENERAL_LEDGER, 'Sales', [self.customer, self.trans_id, self.net]
            )
            append_data(
                GENERAL_LEDGER, 'Sales Tax', [self.customer, self.trans_id, self.tax]
            )
            append_data(
                GENERAL_LEDGER, 'Current Assets', ['', '', '', [self.customer, self.trans_id, self.gross]]
            )
            append_data(
                
            )
