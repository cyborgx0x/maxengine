from .trade_signal import Signal
import os

class Engine():
    '''
    Automate Fill order with a defined set of strategies.
    Order will be send in form of Signal object
    '''
    def __init__(self):
        self.signal_set=[]
        self.login_data={}
    def execute_trade(self) -> None:
        for i in  self.signal_set:
            self.send_order(i)
    def set_signal(self, signal: Signal) -> None:
        self.signal_set.append(signal)
    def send_order(self, order: Signal):
        print(order.get_signal())
        print(self.login_data)
