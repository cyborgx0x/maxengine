from .strategy import Strategy


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
    def compute(self):
        # Define the chain of responsibility
        handler = MovingAverageHandler(
            CandlestickPatternHandler(
                RsiHandler()
            )
        )

        # Check the conditions using the chain of responsibility
        is_downtrend = handler.handle(self._data)
        is_uptrend = handler.handle(self._data)

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
