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

class Computers:
    """
    Computers class
    """
    pass   

class CurrentAsset:
    """
    Current asset class
    """
    def __init__(self, price, sellprice, stock):
        self.price = price
        self.sellprice = sellprice
        self.stock = stock
