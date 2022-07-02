class Sales:
    """
    Class for recording a transaction
    """
    def __init__(self) -> None:
        self.post = []
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

class SoapBarSale(Sales):
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
        super().__init__()