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
    server = FakeServer()
    def __init__(self, symbol:str) -> None:
        self.order = Order()
        if os.getenv("livetrading") != "0":
            '''
            Data for backtesting will be processed here
            signal.server = server
            or signal.data = server.data
            ''' 
            self.data = self.server.data
            self.get_backtesting_data()
            self.order.price = self.server.get_price()
        else:
            self.data.get_mt_data(symbol, mt.TIMEFRAME_D1, datetime.datetime.fromisoformat("2018-01-01"), datetime.datetime.now())
            self._data = self.data.full_data
        self.order.symbol = symbol
    def get_signal(self) -> Order:

        try: 
            self.order.comment = f"{self.__class__.__name__}"
            self.process()
        except IndexError:
            print("process Err!")
        return self.order
    def get_backtesting_data(self) -> None:
        '''
        method for working with different data will stay here
        '''
        self._data = self.server.get_data()
    def process(self, *args, **kwargs) -> None:
        '''
        logic goes here
        '''
        pass


class Trend_Following(Signal):
    def process(self):
        daily_dt = TripleMA(self._data.get("daily"))
        hour_dt = TripleMA(self._data.get("hourly"))
        fif_dt = TripleMA(self._data.get("fifteen"))
        self.order.price = daily_dt.price
        if daily_dt.result == "uptrend" and hour_dt.result == "uptrend":
            self.order.mt_type = "buy"
        if daily_dt.result == "downtrend" and hour_dt.result == "downtrend":
            self.order.mt_type = "sell"


class SingleLine(Signal):
    def process(self):
        
        daily_dt = TripleMA(self._data)
        if daily_dt.result == "uptrend":
            self.order.mt_type = "buy"
        elif daily_dt.result == "downtrend":
            self.order.mt_type = "sell"
        else:
            self.order.mt_type = ""


class MultiTimeframeTrendFollowing(Signal):
    def __init__(self, symbol: str) -> None:
        super().__init__(symbol)
        if os.getenv("livetrading") != "0":
            self.m15_price = self.data.get_data_v2("m15")
            self.h1_price = self.data.get_data_v2("h1")
            self.d1_price = self.data.get_data_v2("d1")
        else:
            print(self.order.symbol)
            print("get price in m15")
            self.m15_price = self.data.get_mt_data(symbol, mt.TIMEFRAME_M15, datetime.datetime.now()-datetime.timedelta(days=3), datetime.datetime.now())
            print("get data in h1")
            self.h1_price = self.data.get_mt_data(symbol, mt.TIMEFRAME_H1, datetime.datetime.now()-datetime.timedelta(days=50), datetime.datetime.now())
            print("get data in d1")
            self.d1_price = self.data.get_mt_data(symbol, mt.TIMEFRAME_D1, datetime.datetime.now()-datetime.timedelta(days=250), datetime.datetime.now())

    def compute_sma(self, history_price):
        f = history_price["close"].to_frame()
        f["SMA50"] = f["close"].rolling(50).mean()
        f["SMA100"] = f["close"].rolling(100).mean()
        f["SMA200"] = f["close"].rolling(200).mean()
        f.dropna(inplace = True)
        return f

    def trend_mature(self, trend_lifetime, period):
        if trend_lifetime > period:
            return False
        else:
            return True
    def trend_early(self, trend_early, period):
        if trend_early:
            return True
        else:
            return False

    def process(self):
        d1_sma = self.compute_sma(self.d1_price)
        h1_sma = self.compute_sma(self.h1_price)
        m15_sma = self.compute_sma(self.m15_price)
        last_d1 = d1_sma.iloc[-1]
        last_h1 = h1_sma.iloc[-1]
        last_m15 = m15_sma.iloc[-1]
        d1_long_condition = last_d1["SMA50"] > last_d1["SMA100"] and last_d1["SMA100"] > last_d1["SMA200"] 
        h1_long_condition = last_h1["SMA50"] > last_h1["SMA100"] and last_h1["SMA100"] > last_h1["SMA200"] 
        m15_long_condition = last_m15["SMA50"] > last_m15["close"] and last_m15["close"] > last_m15["SMA200"] 
        d1_short_condition = last_d1["SMA50"] < last_d1["SMA100"] and last_d1["SMA100"] < last_d1["SMA200"] 
        h1_short_condition = last_h1["SMA50"] < last_h1["SMA100"] and last_h1["SMA100"] < last_h1["SMA200"] 
        m15_short_condition = last_m15["SMA50"] < last_m15["close"] and last_m15["close"] < last_m15["SMA200"] 

        if d1_long_condition and m15_long_condition:
            self.order.mt_type = "buy"
            print("buy criterias met!")
        elif d1_short_condition  and m15_short_condition:
            self.order.mt_type = "sell"
            print("sell criterias met!")
        else:
            self.order.mt_type = ""
        
        



