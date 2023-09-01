from abc import ABC, abstractmethod
from collections import namedtuple
from typing import List

from pandas import DataFrame

Result = namedtuple("Result", ["risk_score", "risk_reward_ratio", "win_rate"])


class Strategy(ABC):
    """
    strategy take the data price of any pair
    """

    risk_score = None
    risk_reward_ratio = None
    win_rate = None

    def __init__(self, data: DataFrame) -> None:
        self._data = data
        super().__init__()

    @abstractmethod
    def compute(self):
        return Result(self.risk_score, self.risk_reward_ratio, self.win_rate)

    @abstractmethod
    def visualize(self):
        ...

    @abstractmethod
    def add_component(self):
        ...


class TechnicalAnalysisDecorator:
    def __init__(self, data):
        self._data = data

    def apply(self):
        pass


class OscillatorDecorator(TechnicalAnalysisDecorator):
    def __init__(self, data, window):
        super().__init__(data)
        self._window = window

    def apply(self):
        rolling_max = self._data["high"].rolling(self._window).max()
        rolling_min = self._data["low"].rolling(self._window).min()
        oscillator = (self._data["close"] - rolling_min) / (rolling_max - rolling_min)
        self._data["Oscillator"] = oscillator
        return self._data


class ConditionHandler:
    def __init__(self, next_handler=None):
        self._next_handler = next_handler

    def handle(self, data):
        pass


class RangeHandler(ConditionHandler):
    def __init__(self, threshold):
        self._threshold = threshold

    def handle(self, data):
        if data["Oscillator"].iloc[-1] < self._threshold:
            return True
        elif data["Oscillator"].iloc[-1] > (1 - self._threshold):
            return True
        else:
            return self._next_handler.handle(data) if self._next_handler else False


class RangeTrading(Strategy):
    def __init__(self, data: DataFrame, window: int, threshold: float) -> None:
        # Apply technical analysis decorators
        data = OscillatorDecorator(data, window).apply()

        super().__init__(data)

        # Define the chain of responsibility
        self._handler = RangeHandler(threshold)

    def compute(self):
        # Check the conditions using the chain of responsibility
        is_long = self._handler.handle(self._data)
        is_short = self._handler.handle(self._data)

        # Check for long and short positions
        if is_long:
            return dict(
                is_long=True,
                price=0,
                probability=0,
                rr_ratio=0.2,
            )

        if is_short:
            return dict(
                is_short=True,
                price=0,
                probability=0,
                rr_ratio=0.2,
            )

        return super().compute()

    def visualize(self):
        self._data

    def add_component(self):
        return super().add_component()
