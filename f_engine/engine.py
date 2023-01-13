from .trade_signal import Signal
import os
from .server import FakeServer
from datetime import date
from .meta_wrapper import MT5Account
from .order import Order
from typing import List

class Engine():
    '''
    Automate Fill order with a defined set of strategies.
    Order will be send in form of Signal object
    '''
    signal_set:List[Signal] = []
    order_list = []
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
        order.time = self.get_time()
        if not order.type == "":
            self.server.get_order(order)
        return True

    def send_order_mt5(self, order: Order) -> bool:
        ''''
        check logic here
        '''
        o = order.get_mt5_order()
        status = self.mt5.execute_order(o)
        self.order_list.append(o)
        print(f"sending order: {order}")
        if status:
            print("XXX")
    def get_time(self) -> date:
        return self.time.current_time

    def connect(self, server: FakeServer) -> bool:
        self.server = server
        return True

    def connect_mt5(self, mt5: MT5Account) -> bool:
        self.mt5 = mt5

        return True
