import MetaTrader5 as mt
import numpy as np 
import pandas as pd
import datetime

class Account():
    def __init__(self, **kwarg):
        self.account_number = kwarg["account_number"]
        self.password = kwarg["password"]
        self.server = kwarg["server"]
    def login(self):
        mt.login(self.account_number, self.password, self.server)
    def start(self):
        mt.initialize()
    def info(self):
        return mt.account_info()
    def get_all_pair(self):
        symbols = mt.symbols_get("*USDm")
        r = []
        for s in symbols:
            if s.trade_mode != 0:
                r.append(s.name)
        return r
            
    def get_history_price(self, pair_name, timeframe, n):
        history =  mt.copy_rates_range(pair_name, timeframe, datetime.datetime.now()-datetime.timedelta(n), datetime.datetime.now())
        history_frame = pd.DataFrame(history)
        return history_frame
    def get_current_price(self, pair_name):
        price = mt.symbol_info_tick(pair_name).ask
        return price
    def trade(self, pair, price, order_type):
        point = mt.symbol_info(pair).point
        print(point)
        if order_type == "buy":
            ordt = mt.ORDER_TYPE_BUY
            sl = price - 1000 * point
            tp = price + 1000 * point
        else:
            ordt = mt.ORDER_TYPE_SELL
            sl = price + 1000 * point
            tp = price - 1000 * point
        x = {
            "action": mt.TRADE_ACTION_DEAL,
            "symbol": pair,
            "volume": 0.1,
            "type": ordt,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": 20,
            "magic": 234300,
            "comment": "python script open",
            "type_time": mt.ORDER_TIME_GTC,
            "type_filling": mt.ORDER_FILLING_IOC,
        }
        result = mt.order_send(x)
        print(result)
        return result