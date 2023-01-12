from typing import Dict
from .ta import TripleMA
class Signal(object):
    def __init__(self, data: Dict) -> None:
        self._data = data
        self.price = ""
        self.order_type = ""
    def get_signal(self):
        self.trend()
        return {
            "symbol": self._data.get("symbol"),
            "order_type": self.order_type,
            "price": self.price,
        }
    def trend(self) -> None:
        pass


class Trend_Following(Signal):
    def trend(self):
        daily_dt = TripleMA(self._data.get("daily"))
        hour_dt = TripleMA(self._data.get("hourly"))
        fif_dt = TripleMA(self._data.get("fifteen"))
        self.price = daily_dt.price
        if daily_dt.get_result() == "uptrend" and hour_dt.get_result() == "uptrend":
            self.order_type = "buy"
        if daily_dt.get_result() == "downtrend" and hour_dt.get_result() == "downtrend":
            self.order_type = "sell"
        
class SingleLine(Signal):
    def trend(self):
        daily_dt = TripleMA(self._data.get("daily"))
        try:
            self.price = daily_dt.price
        except:
            print("No Price")
        if daily_dt.get_result()["result"] == "uptrend":
            self.order_type = "buy"
        if daily_dt.get_result()["result"] == "downtrend":
            self.order_type = "sell"