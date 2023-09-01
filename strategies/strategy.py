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


class StrategySet:
    collection: List[Strategy]

    def compute_risk(self):
        for st in self.collection:
            st.compute()

    def visualize(self):
        for st in self.collection:
            st.visualize()

    def result(self):
        ...
