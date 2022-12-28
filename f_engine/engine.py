from .trade_signal import Signal
import os

class Engine():
    def __init__(self, data):
        self._data = data
        self.startState = None
    def run_backtest(self):
        for row in self._data:
            print("loop through the data")
            self.price = ""
    def execute_trade(self, signal: Signal) -> None:
        
        print(signal.get_signal())
    def start(self):
        self.state = self.startState
    def step(self, newInput):
        (s, o) = self.getNextValue(self.state, newInput)
        self.state = s
        return o
    def getNextValue(self, state, newState):
        return state, newState
    def tranduce(self, inputs):
        self.start()
        return [self.step(inp) for inp in inputs]