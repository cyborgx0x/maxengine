import MetaTrader5 as mt
import numpy as np
import pandas as pd
import datetime
from .order import Order


class MT5Account():

    '''
    Provide a wrapper to work with MT5
    '''
    def start(self):
        mt.initialize()
    def login(self):
        mt.login(self.account_number, self.password, self.server)

    def info(self) -> None:
        return mt.account_info()

    def get_all_pair(self):
        symbols = mt.symbols_get("*USDm")
        r = []
        for s in symbols:
            if s.trade_mode != 0:
                r.append(s.name)
        return r

    def get_history_price(self, *args, **kwargs):
        history = mt.copy_rates_range(*args, **kwargs)
        history_frame = pd.DataFrame(history)
        return history_frame

    def get_current_price(self, pair_name):
        print(pair_name)
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
        return {
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

    def execute_order(self, order) -> None:

        result = mt.order_send(order)
        print("XXX")
        return result
