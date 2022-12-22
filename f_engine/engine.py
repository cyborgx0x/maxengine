from .trade_signal import Signal
import os

class Engine():
    def __init__(self, data):
        self._data = data
    def run_backtest(self):
        for row in self._data:
            print("loop through the data")
            self.price = ""
    def execute_trade(self, signal: Signal) -> None:
        
        print(signal.get_signal())
    def plot(self):
        pass
    def cache(self):
        pass