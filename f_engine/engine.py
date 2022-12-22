from .signal import Signal

class Engine():
    def __init__(self, data):
        self._data = data
    def run_backtest(self):
        for row in self._data:
            print("loop through the data")
    def execute_trade(self, signal: Signal) -> None:
        return True

def execute_trade(signal):
    if price == signal.price:
        return True
    else:
        return False

