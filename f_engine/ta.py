class Indicator():
    def __init__(self, data):
        self.history_data = data
        self.result = "No Data"
        try:
            self.trend()
        except ValueError:
            print("Data too small")
    def get_result(self):
        return {
            "result": self.result,
            "data": self.history_data
        }


class TripleMA(Indicator):
    def process(self):
        self.triple_ma = self.history_data[["Close"]].copy()
        self.triple_ma["SMA50"] = self.triple_ma["Close"].rolling(5).mean()
        self.triple_ma["SMA100"] = self.triple_ma["Close"].rolling(15).mean()
        self.triple_ma["SMA200"] = self.triple_ma["Close"].rolling(30).mean()
        self.triple_ma.dropna(inplace=True)
        return 0

    def trend(self):
        self.process()
        last_price = self.triple_ma.tail(1)
        uptrend = last_price["SMA50"].item() > last_price["SMA100"].item(
        ) and last_price["SMA100"].item() > last_price["SMA200"].item()
        downtrend = last_price["SMA50"].item() < last_price["SMA100"].item(
        ) and last_price["SMA100"].item() > last_price["SMA200"].item()
        self.price = last_price["Close"].item()
        buy = self.price > last_price["SMA200"].item(
        ) and self.price < last_price["SMA50"].item()
        sell = self.price < last_price["SMA200"].item(
        ) and self.price > last_price["SMA50"].item()
        if uptrend:
            self.result = "uptrend"
        if downtrend:
            self.result = "downtrend"
        if not uptrend and not downtrend:
            self.result = "sideway"
