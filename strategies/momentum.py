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


class RsiDecorator(TechnicalAnalysisDecorator):
    def __init__(self, data, window):
        super().__init__(data)
        self._window = window

    def apply(self):
        delta = self._data["close"].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(self._window).mean()
        avg_loss = loss.rolling(self._window).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        self._data["RSI"] = rsi
        return self._data


class MacdDecorator(TechnicalAnalysisDecorator):
    def __init__(self, data, fast_window, slow_window, signal_window):
        super().__init__(data)
        self._fast_window = fast_window
        self._slow_window = slow_window
        self._signal_window = signal_window

    def apply(self):
        exp1 = self._data["close"].ewm(span=self._fast_window, adjust=False).mean()
        exp2 = self._data["close"].ewm(span=self._slow_window, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=self._signal_window, adjust=False).mean()
        self._data["MACD"] = macd
        self._data["Signal"] = signal
        return self._data


class ConditionHandler:
    def __init__(self, next_handler=None):
        self._next_handler = next_handler

    def handle(self, data):
        pass


class RsiHandler(ConditionHandler):
    def __init__(self, threshold):
        self._threshold = threshold

    def handle(self, data):
        if data["RSI"].iloc[-1] > self._threshold:
            return True
        else:
            return self._next_handler.handle(data) if self._next_handler else False


class MacdHandler(ConditionHandler):
    def handle(self, data):
        if data["MACD"].iloc[-1] > data["Signal"].iloc[-1]:
            return True
        else:
            return self._next_handler.handle(data) if self._next_handler else False


class MomentumTrading(Strategy):
    def __init__(self, data: DataFrame, rsi_window: int, macd_fast_window: int, macd_slow_window: int, macd_signal_window: int, rsi_threshold: float) -> None:
        # Apply technical analysis decorators
        data = RsiDecorator(data, rsi_window).apply()
        data = MacdDecorator(data, macd_fast_window, macd_slow_window, macd_signal_window).apply()

        super().__init__(data)

        # Define the chain of responsibility
        self._handler = RsiHandler(rsi_threshold)
        self._handler = MacdHandler(self._handler)

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
