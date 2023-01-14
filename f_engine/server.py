import pandas
import time
from .order import  Order
from .data import Data
from .time_machine import TimeMachine, SingletonMeta

class Account():
    def __init__(self, capital: int = 0, margin: int = 0, currency: str = "USD") -> None:
        self.capital = capital
        self.margin = margin
        self.currency = currency
    def position(self):
        pass

class FakeServer(metaclass=SingletonMeta):

    account = Account(1000, 20)
    spread = 7
    lag = 30
    data = Data()
    time = TimeMachine()

    def __init__(self, ) -> None:
        self.order = []

    def execute_trade(self) -> None:
        for i in self.order:
            self.fill_order(i)
        if self.account.margin < 1:
            return "Not enough Capital"

    def fill_order(self, order: Order):
        if order.mt_type == "sell":
            # order.price -= self.get_spead()
            print(order)
            print(self.get_price())
        if order.mt_type == "buy":
            # order.price += self.get_spead()
            print(order)
    
    def get_data(self):
        end_date =  self.time.current_time
        begin_time = self.time.begin_time
        return self.data.yahoo_data[begin_time:end_date].copy(deep=True)

    def get_order(self, order):
        self.lag_time()
        self.order.append(order)

    def get_price(self):
        current_row = self.data.yahoo_data[self.time.current_time.isoformat(
        ):self.time.current_time.isoformat()].tail(1)
        try:
            return current_row["close"].values[0]
        except:
            return None
    def get_spead(self):
        return self.spread/1000

    def lag_time(self):
        time.sleep(self.lag/1000)