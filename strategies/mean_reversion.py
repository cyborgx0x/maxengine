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


class BollingerBandsDecorator(TechnicalAnalysisDecorator):
    def __init__(self, data, window, num_std):
        super().__init__(data)
        self._window = window
        self._num_std = num_std

    def apply(self):
        rolling_mean = self._data["close"].rolling(self._window).mean()
        rolling_std = self._data["close"].rolling(self._window).std()
        upper_band = rolling_mean + (rolling_std * self._num_std)
        lower_band = rolling_mean - (rolling_std * self._num_std)
        self._data["UpperBand"] = upper_band
        self._data["LowerBand"] = lower_band
        return self._data


class ConditionHandler:
    def __init__(self, next_handler=None):
        self._next_handler = next_handler

    def handle(self, data):
        pass


class MovingAverageHandler(ConditionHandler):
    def __init__(self, window):
        self._window = window

    def handle(self, data):
        if data[f"SMA{self._window}"].iloc[-1] > data["close"].iloc[-1]:
            return True
        else:
            return self._next_handler.handle(data) if self._next_handler else False


class BollingerBandsHandler(ConditionHandler):
    def __init__(self, num_std):
        self._num_std = num_std

    def handle(self, data):
        if data["close"].iloc[-1] < data["LowerBand"].iloc[-1]:
            return True
        elif data["close"].iloc[-1] > data["UpperBand"].iloc[-1]:
            return True
        else:
            return self._next_handler.handle(data) if self._next_handler else False


class MeanReversionTrading(Strategy):
    def __init__(self, data: DataFrame, ma_windows: List[int], bb_window: int, bb_num_std: int) -> None:
        # Apply technical analysis decorators
        for window in ma_windows:
            data = MovingAverageDecorator(data, window).apply()
        data = BollingerBandsDecorator(data, bb_window, bb_num_std).apply()

        super().__init__(data)

        # Define the chain of responsibility
        self._handler = MovingAverageHandler(ma_windows[0])
        for window in ma_windows[1:]:
            self._handler = MovingAverageHandler(window, self._handler)
        self._handler = BollingerBandsHandler(bb_num_std, self._handler)

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

