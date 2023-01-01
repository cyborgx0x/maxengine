
class Account():
    def __init__(self, capital:int=0, margin:int=0, currency:str="USD") -> None:
        self.capital = capital
        self.margin = margin
        self.currency = currency

class FakeServer():
    account = Account(1000, 20)
    def __init__(self) -> None:
        pass
    def execute_trade(self, request: str) -> None:
        if self.account.margin < 1:
            return "Not enough Capital"
    def get_price(self, pair):
        pass
    def filling_order(self, pair)
    