import pandas
import time
from .order import  Order
class Account():
    def __init__(self, capital: int = 0, margin: int = 0, currency: str = "USD") -> None:
        self.capital = capital
        self.margin = margin
        self.currency = currency
    def position(self):
        pass

class FakeServer():

    account = Account(1000, 20)
    spread = 7
    lag = 30

    def __init__(self, ) -> None:
        daily_data = ""
        self.order = []

    def execute_trade(self) -> None:
        for i in self.order:
            self.fill_order(i)
        if self.account.margin < 1:
            return "Not enough Capital"

    def fill_order(self, order: Order):
        if order.type == "sell":
            # order.price -= self.get_spead()
            print(order)
        if order.type == "buy":
            # order.price += self.get_spead()
            print(order)
    
    def get_data(self, start_date, end_date, interval):
        if interval == "1D":
            return self.daily_data.loc[start_date:end_date]

    def get_order(self, order):
        self.lag_time()
        self.order.append(order)

    def get_price(self):

        current_row = self.daily_data[self.time.current_time.isoformat(
        ):self.time.current_time.isoformat()].tail(1)
        try:
            return current_row["Close"].item()
        except:
            return None
    def get_spead(self):
        return self.spread/1000
    def get_time(self):
        return self.time.current_time
    def lag_time(self):
        time.sleep(self.lag/1000)