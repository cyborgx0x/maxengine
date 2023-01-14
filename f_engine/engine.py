'''
provide the way to work with both backtesting and live trading

Send order to the Fake Server for the purpose of backtesting
Send order to the any live trading software
'''

from .trade_signal import Signal
import os
from .server import FakeServer
from datetime import date
from .meta_wrapper import MT5Account
from .order import Order
from typing import List
from .time_machine import TimeMachine


class Engine():
    '''
    Automate Fill order with a defined set of strategies.
    Order will be send in form of Signal object
    '''
    signal_set:List[Signal] = []
    order_list = []
    time = TimeMachine()
    def execute_trade(self, mt5=False) -> bool:
        '''
        execute all Signal from signal set to get order
        '''
        if mt5 == True:
            for i in self.signal_set:
                self.send_order_mt5(i.get_signal())
        else:
            for i in self.signal_set:
                self.send_order(i.get_signal())
        return True
        
    def send_order(self, order: Order) -> bool:
        if order == None:
            return False
        else:
            order.time = self.time.current_time
            
            if not order.mt_type == "":
                self.server.get_order(order)
                self.order_list.append(order)
            return True

    def send_order_mt5(self, order: Order) -> bool:
        if order == None: 
            return False
        if order.mt_type == "buy" or order.mt_type == "sell":
            self.mt5.execute_order(order)
            self.order_list.append(order.get_mt5_order())
        else:
            return False



    def connect(self, server: FakeServer) -> bool:
        self.server = server
        return True

    def connect_mt5(self, mt5: MT5Account) -> bool:
        self.mt5 = mt5

        return True
