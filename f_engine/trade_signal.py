from typing import Dict
from .ta import TripleMA
from .order import Order
from pandas import DataFrame

class Signal():
    order = Order()
    def __init__(self, data: DataFrame) -> None:
        self._data = data
        self.order.price = ""
    def get_signal(self) -> Order:
        self.trend()
        self.order.symbol = self._data.get("symbol")
        if self.order.mt_type == "":
            return None
        else:
            return self.order

    def trend(self) -> None:
        '''
        logic goes here
        '''
        pass


class Trend_Following(Signal):
    def trend(self):
        daily_dt = TripleMA(self._data.get("daily"))
        hour_dt = TripleMA(self._data.get("hourly"))
        fif_dt = TripleMA(self._data.get("fifteen"))
        self.order.price = daily_dt.price
        if daily_dt.result == "uptrend" and hour_dt.result == "uptrend":
            self.order.mt_type = "buy"
        if daily_dt.result == "downtrend" and hour_dt.result == "downtrend":
            self.order.mt_type = "sell"


class SingleLine(Signal):
    def trend(self):
        self.order.comment = f"Order Result from {self.__class__.__name__}"
        daily_dt = TripleMA(self._data.get("daily"))
        if daily_dt.result == "uptrend":
            self.order.mt_type = "buy"
        elif daily_dt.result == "downtrend":
            self.order.mt_type = "sell"
        else:
            self.order.mt_type = ""