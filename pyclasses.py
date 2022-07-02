class NonCurrentAsset:
    """
    Non-current asset class
    """
    def __init__(self, price, stock, depreciation):
        """class attributes

        Args:
            price (int/float): buying price of item
            stock (int): amount owned
        """
        self.price = price
        self.stock = stock
        self.depreciation = depreciation 
        self.glaccount = 'Non-Current Assets'

class Computers(NonCurrentAsset):
    """
    Computers class
    """
    pass   

class CurrentAsset:
    """
    Current asset class
    """
    def __init__(self, glaccount):
        self.glaccounts = ['Current Assets', glaccount]

class SaleOfCurrentAsset(CurrentAsset):
    """
    Class for sales of current assets
    """
    def __init__(self, glaccount, gross):
        super().__init__(glaccount)
        self.tax = 0.25*gross
        self.net = 0.75*gross
        self.gross = gross
    def money_amounts(self):
        """
        Returns:
            list: a list of amounts related to sale
        """
        return [self.net, self.tax, self.gross]

class SoapBarsSale(SaleOfCurrentAsset):
    """
    Class for soap bars
    Args:
        SaleOfCurrentAsset (class): handles the sale of soap bar
    """
    def __init__(self, amount, crdr, bankcash):
        """
        Args:
            amount (int): Amount sold
            crdr (str): wether sale was on credit or debit
            bankcash (str): wether sale was in bank or cash
        """
        self.sellprice = 10
        self.total = self.sellprice * amount
        if crdr == 'cr':
            self.account = 'Trade Receivables'
        elif bankcash == 'bank':
            self.account = 'Bank'
        else:
            self.account = 'Cash'
        super().__init__(self.account, self.total)
