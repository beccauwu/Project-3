from funcs import ACCOUNTS, GENERAL_LEDGER, RECEIVABLES, STOCK, choose_customer, append_data, gen_rand_list, cash_or_credit, get_date

class Sales():
    """
    Class for recording a transaction
    """
    def __init__(self) -> None:
        self.date = []
        self.trans_id = None
        self.type = None
        self.customer = []

    

class SoapBarSale(Sales):
    """
    Class for soap bar sales

    Args:
        Sales (class): processes data
    """
    def __init__(self) -> None:
        self.price = 6
        self.amount = None
        Sales.__init__(self)

class LiquidSoapSale(Sales):
    """
    Class for liquid soap sales

    Args:
        Sales (class): processes data
    """
    def __init__(self, amount= None) -> None:
        super().__init__(5, amount)
class CoconutOilSale(Sales):
    """
    Class for coconut oil sales

    Args:
        Sales (class): processes data
    """
    def __init__(self, amount= None) -> None:
        super().__init__(7, amount)
class LuteSale(Sales):
    """
    Class for sodium hydroxide sales

    Args:
        Sales (class): processes data
    """
    def __init__(self, amount= None) -> None:
        super().__init__(20, amount)
