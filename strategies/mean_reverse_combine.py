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


class MovingAverageDecorator(TechnicalAnalysisDecorator):
    def __init__(self, data, window):
        super().__init__(data)
        self._window = window

    def apply(self):
        self._data[f"SMA{self._window}"] = self._data["close"].rolling(self._window).mean()
        return self._data


class CandlestickPatternDecorator(TechnicalAnalysisDecorator):
    def __init__(self, data):
        super().__init__(data)

    def apply(self):
        # Check for bullish candlestick patterns
        if self._data["close"].iloc[-2] < self._data["open"].iloc[-2] and self._data["close"].iloc[-1] > self._data["open"].iloc[-1]:
            self._data["bullish_candlestick"] = True
        else:
            self._data["bullish_candlestick"] = False

        # Check for bearish candlestick patterns
        if self._data["close"].iloc[-2] > self._data["open"].iloc[-2] and self._data["close"].iloc[-1] < self._data["open"].iloc[-1]:
            self._data["bearish_candlestick"] = True
        else:
            self._data["bearish_candlestick"] = False

        return self._data


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


class ConditionHandler:
    def __init__(self, next_handler=None):
        self._next_handler = next_handler

    def handle(self, data):
        pass


class MovingAverageHandler(ConditionHandler):
    def handle(self, data):
        if (
            data["SMA100"].iloc[-1] > data["SMA50"].iloc[-1]
            and data["SMA200"].iloc[-1] > data["SMA100"].iloc[-1]
        ):
            return True
        else:
            return self._next_handler.handle(data) if self._next_handler else False


class CandlestickPatternHandler(ConditionHandler):
    def handle(self, data):
        if data["bullish_candlestick"].iloc[-1]:
            return True
        elif data["bearish_candlestick"].iloc[-1]:
            return True
        else:
            return self._next_handler.handle(data) if self._next_handler else False


class RsiHandler(ConditionHandler):
    def handle(self, data):
        if data["RSI"].iloc[-1] > 70:
            return True
        elif data["RSI"].iloc[-1] < 30:
            return True
        else:
            return self._next_handler.handle(data) if self._next_handler else False


class MeanReverse(Strategy):
    def __init__(self, data: DataFrame) -> None:
        # Apply technical analysis decorators
        data = MovingAverageDecorator(data, 50).apply()
        data = MovingAverageDecorator(data, 100).apply()
        data = MovingAverageDecorator(data, 200).apply()
        data = CandlestickPatternDecorator(data).apply()
        data = RsiDecorator(data, 14).apply()

        super().__init__(data)

        # Define the chain of responsibility
        self._handler = MovingAverageHandler(
            CandlestickPatternHandler(
                RsiHandler()
            )
        )

    def compute(self):
        # Check the conditions using the chain of responsibility
        is_downtrend = self._handler.handle(self._data)
        is_uptrend = self._handler.handle(self._data)

        # Check for downtrend and reversal
        if is_downtrend:
            return dict(
                is_downtrend=True,
                price=0,
                probability=0,
                rr_ratio=0.2,
            )

        # Check for uptrend and reversal
        if is_uptrend:
            return dict(
                is_uptrend=True,
                price=0,
                probability=0,
                rr_ratio=0.2,
            )

        return super().compute()

    def visualize(self):
        self._data

    def add_component(self):
        return super().add_component()
