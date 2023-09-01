from .strategy import Strategy


class MeanReverse(Strategy):
    def compute(self):
        is_uptrend = False
        is_downtrend = False
        is_reverse = False

        self.triple_ma = self._data[["close"]].copy()
        self.triple_ma["SMA50"] = self.triple_ma["close"].rolling(50).mean()
        self.triple_ma["SMA100"] = self.triple_ma["close"].rolling(100).mean()
        self.triple_ma["SMA200"] = self.triple_ma["close"].rolling(200).mean()
        self.triple_ma.dropna(inplace=True)

        if (
            self.triple_ma["SMA100"] > self.triple_ma["SMA50"]
            and self.triple_ma["SMA200"] > self.triple_ma["SMA100"]
        ):
            is_downtrend = True
        if (
            self.triple_ma["SMA100"] < self.triple_ma["SMA50"]
            and self.triple_ma["SMA200"] < self.triple_ma["SMA100"]
        ):
            is_uptrend = True

        # Check for bullish candlestick patterns
        if self._data["close"].iloc[-2] < self._data["open"].iloc[-2] and self._data["close"].iloc[-1] > self._data["open"].iloc[-1]:
            is_reverse = True

        # Check for bearish candlestick patterns
        if self._data["close"].iloc[-2] > self._data["open"].iloc[-2] and self._data["close"].iloc[-1] < self._data["open"].iloc[-1]:
            is_reverse = True

        # Check for RSI or MACD indicators
        # ...

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
