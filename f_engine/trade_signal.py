'''
This Module contain various Strategy

Each Strategy should return a kind of order to the process further. 
in live trading the data will be process from trading software
in backtesting the data will be process from the engine. 

'''
import datetime
from typing import Dict
from .ta import TripleMA
from .server import FakeServer
from .order import Order
from pandas import DataFrame
from .data import Data
import MetaTrader5 as mt
import os
class Signal():
    data = Data()
    order = Order()
    server:FakeServer
    def __init__(self, symbol:str) -> None:
        if os.getenv("livetrading") != 0:
            '''
            Data for backtesting will be processed here
            signal.server = server
            ''' 
            
        self.data.get_mt_data(symbol, mt.TIMEFRAME_D1, datetime.datetime.fromisoformat("2018-01-01"), datetime.datetime.now())
        self.order.symbol = symbol
        self._data = self.data.full_data
        self.order.price = ""
    def get_signal(self) -> Order:
        self.trend()
        if self.order.mt_type == "":
            return None
        else:
            return self.order
    def get_backtesting_data(self):
        self._data = self.server.get_data()
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
        daily_dt = TripleMA(self._data)
        if daily_dt.result == "uptrend":
            self.order.mt_type = "buy"
        elif daily_dt.result == "downtrend":
            self.order.mt_type = "sell"
        else:
            self.order.mt_type = ""