"""
provide the way to work with both backtesting and live trading

Send order to the Fake Server for the purpose of backtesting
Send order to the any live trading software
"""

import os
from datetime import date
from typing import List

from .meta_wrapper import MT5Account
from .order import Order
from .server import FakeServer
from .time_machine import TimeMachine
from .trade_signal import Signal


class Engine:
    """
    ## Engine

    The Engine will process and maintain several trading strategies. Based on each strategy, it will get the signal, apply the filter. If the signal pass the filter, it will execute the trade.
    """

    signal_set: List[Signal] = []
    order_list = []
    time = TimeMachine()

    def show_instrument_condition(self):
        for signal in self.signal_set:
            signal.get_signal()

    def collect_signal(self):
        for signal in self.signal_set:
            self.order_list.append(signal.get_signal())

    def apply_filter(self):
        for order in self.order_list:
            order.filter()

    def execute_trade(self, mt5=False) -> bool:
        """
        execute all Signal from signal set to get order
        """
        if mt5 == True:
            for i in self.signal_set:
                self.send_order_mt5(i.get_signal())
        else:
            for i in self.signal_set:
                self.send_order(i.get_signal())
        return True

    def send_order(self, order: Order) -> bool:
        order.time = self.time.current_time

        if order.mt_type == "buy" or order.mt_type == "sell":
            self.server.get_order(order)
            self.order_list.append(order)
        return True

    def send_order_mt5(self, order: Order) -> bool:
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
