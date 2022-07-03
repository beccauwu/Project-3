from funcs import ACCOUNTS, GENERAL_LEDGER, RECEIVABLES, choose_customer, append_data, gen_rand_list

class Sales():
    """
    Class for recording a transaction
    """
    def __init__(self, price) -> None:
        self.date = input('Enter transaction date: (DD.MM.)')
        self.customer = choose_customer()
        self.type = None
        self.trans_id = 'S'
        self.inv_no = f"INV{gen_rand_list(2)}"
        self.product = product_menu()
        self.amount = self.product[1]
        self.gross = price
    def credit_sale(self) -> None:
        """
        Credit sale method
        - type 1
        - adds signifier for credit in transid
        """
        print('initiated credit sale method')
        self.type = 1
        self.trans_id += 'C'
        self.trans_id += str(self.customer[0])[0]
        self.trans_id += gen_rand_list(3)
    def cash_sale(self) -> None:
        """
        Cash sale method
        - type 2
        - adds signifier for debit in transid
        """
        self.type = 2
        self.trans_id += 'D'
        self.trans_id += str(self.customer[0])[0]
        self.trans_id += gen_rand_list(3)

    def write_transaction(self):
        """
        Writes transaction to accounts
        """
        if self.type == 1:
            append_data(
                GENERAL_LEDGER, 'Trade Receivables',
                [self.customer, self.trans_id, SoapBarSale.gross]
                )
            append_data(
                GENERAL_LEDGER, 'Current Assets',
                ['', '', '', self.customer, self.trans_id, self.gross]
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
                GENERAL_LEDGER,
                'Current Assets', ['', '', '', [self.customer, self.trans_id, self.gross]]
            )
            append_data(
                ACCOUNTS, 'cash', [self.date, self.customer[2], self.customer[1], self.gross]
            )

class SoapBarSale(Sales):
    """
    Class for soap bar sales

    Args:
        Sales (class): processes data
    """
    def __init__(self) -> None:
        self.price = 6
        super().__init__(self.price)

class LiquidSoapSale(Sales):
    """
    Class for soap bar sales

    Args:
        Sales (class): processes data
    """
    def __init__(self) -> None:
        self.price = 5
        super().__init__(self.price)
class CoconutOilSale(Sales):
    """
    Class for soap bar sales

    Args:
        Sales (class): processes data
    """
    def __init__(self) -> None:
        self.price = 7
        super().__init__(self.price)
class LuteSale(Sales):
    """
    Class for soap bar sales

    Args:
        Sales (class): processes data
    """
    def __init__(self) -> None:
        self.price = 20
        super().__init__(self.price)

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
