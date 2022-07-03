from funcs import ACCOUNTS, GENERAL_LEDGER, RECEIVABLES, STOCK, choose_customer, append_data, gen_rand_list, cash_or_credit

class Sales():
    """
    Class for recording a transaction
    """
    def __init__(self, price, amount) -> None:
        self.date = input('Enter transaction date: (DD.MM.)')
        self.customer = choose_customer()
        self.type = cash_or_credit()
        self.trans_id = 'S'
        self.inv_no = f"INV{gen_rand_list(2)}"
        self.amount = amount
        self.gross = price * amount
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
                [self.customer, self.trans_id, self.gross]
                )
            append_data(
                GENERAL_LEDGER, 'Current Assets',
                ['', '', '', self.customer, self.trans_id, self.gross]
                )
            append_data(
                RECEIVABLES, self.customer, ['Invoice', self.gross, self.inv_no]
                )
            append_data(
                ACCOUNTS, 'sdb',
                [self.date, self.customer, self.gross * 0.75, self.gross * 0.25, self.gross]
                )
        if self.type == 2:
            append_data(
                GENERAL_LEDGER, 'Sales', [self.customer, self.trans_id, self.gross * 0.75]
            )
            append_data(
                GENERAL_LEDGER, 'Sales Tax', [self.customer, self.trans_id, self.gross * 0.25]
            )
            append_data(
                GENERAL_LEDGER,
                'Current Assets', ['', '', '', [self.customer, self.trans_id, self.gross]]
            )
            append_data(
                ACCOUNTS, 'cash', [self.date, self.customer[1], self.customer[0], self.gross]
            )

class SoapBarSale(Sales):
    """
    Class for soap bar sales

    Args:
        Sales (class): processes data
    """
    print('SoapBar called')
    def __init__(self, amount= None) -> None:
        self.price = 6
        self.amount = amount
        super().__init__(self.price, amount)

class LiquidSoapSale(Sales):
    """
    Class for soap bar sales

    Args:
        Sales (class): processes data
    """
    print('LiquidSoap called')
    def __init__(self, amount= None) -> None:
        self.price = 5
        super().__init__(self.price, amount)
class CoconutOilSale(Sales):
    """
    Class for soap bar sales

    Args:
        Sales (class): processes data
    """
    print('Coconut called')
    def __init__(self, amount= None) -> None:
        self.price = 7
        super().__init__(self.price, amount)
class LuteSale(Sales):
    """
    Class for soap bar sales

    Args:
        Sales (class): processes data
    """
    print('Lute called')
    def __init__(self, amount= None) -> None:
        self.price = 20
        super().__init__(self.price, amount)

