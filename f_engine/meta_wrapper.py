import MetaTrader5 as mt
import numpy as np
import pandas as pd
import datetime
from .order import Order


class MT5Account():

    '''
    Provide an easy way to work with MT5, Type Hint Include!!!
    '''
    account_number:int
    password:str
    server:str
    
    def start(self):
        mt.initialize()
    def login(self):
        authorized = mt.login(int(self.account_number), password = self.password, server=self.server)
        
        if authorized:
            print("connected to account #{}".format(self.account_number))
        else:
            print("failed to connect at account #{}, error code: {}".format(self.account_number, mt.last_error()))

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
        price = mt.symbol_info_tick(pair_name).ask
        return price

    def execute_order(self, order: Order) -> None:
        print(f"send request {order.symbol}")
        request = order.get_mt5_order()
        print(f"request:{request}")
        result = mt.order_send(request)
        print(f"Result for order is: {result}")
        return result
