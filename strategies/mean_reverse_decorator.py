from .strategy import Strategy


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


class MeanReverse(Strategy):
    def compute(self):
        is_uptrend = False
        is_downtrend = False
        is_reverse = False

        # Apply technical analysis decorators
        data = self._data.copy()
        data = MovingAverageDecorator(data, 50).apply()
        data = MovingAverageDecorator(data, 100).apply()
        data = MovingAverageDecorator(data, 200).apply()
        data = CandlestickPatternDecorator(data).apply()
        data = RsiDecorator(data, 14).apply()

        # Check for uptrend and downtrend
        if (
            data["SMA100"].iloc[-1] > data["SMA50"].iloc[-1]
            and data["SMA200"].iloc[-1] > data["SMA100"].iloc[-1]
        ):
            is_downtrend = True
        if (
            data["SMA100"].iloc[-1] < data["SMA50"].iloc[-1]
            and data["SMA200"].iloc[-1] < data["SMA100"].iloc[-1]
        ):
            is_uptrend = True

        # Check for bullish and bearish candlestick patterns
        if data["bullish_candlestick"].iloc[-1]:
            is_reverse = True
        if data["bearish_candlestick"].iloc[-1]:
            is_reverse = True

        # Check for RSI indicator
        if data["RSI"].iloc[-1] > 70:
            is_reverse = True
        if data["RSI"].iloc[-1] < 30:
            is_reverse = True

        if is_downtrend and is_reverse:
            return dict(
                is_downtrend=True,
                price=0,
                probability=0,
                rr_ratio=0.2,
            )
        if is_uptrend and is_reverse:
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
