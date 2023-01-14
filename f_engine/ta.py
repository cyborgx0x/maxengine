class TripleMA():
    result = ""
    trend = -1
    def __init__(self, data) -> None:
        self.data = data
        try:
            self.trend_()
        except ValueError:
            print("Data too small")
    def process(self):
        self.triple_ma = self.data[["close"]].copy()
        self.triple_ma["SMA50"] = self.triple_ma["close"].rolling(5).mean()
        self.triple_ma["SMA100"] = self.triple_ma["close"].rolling(15).mean()
        self.triple_ma["SMA200"] = self.triple_ma["close"].rolling(30).mean()
        self.triple_ma.dropna(inplace=True)
        return 0

    def trend_(self):
        self.process()
        last_price = self.triple_ma.tail(1)
        uptrend = last_price["SMA50"].item() > last_price["SMA100"].item(
        ) and last_price["SMA100"].item() > last_price["SMA200"].item()
        downtrend = last_price["SMA50"].item() < last_price["SMA100"].item(
        ) and last_price["SMA100"].item() > last_price["SMA200"].item()
        self.price = last_price["close"].item()
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

def sma_trend(history_price):
    f = history_price["close"].to_frame()
    f.dropna(inplace = True)
    f["SMA30"] = f["close"].rolling(30).mean()
    f["SMA50"] = f["close"].rolling(50).mean()
    f["SMA100"] = f["close"].rolling(100).mean()
    f["SMA200"] = f["close"].rolling(200).mean()
    close = f.iloc[-1]["close"]
    sma50 = f.iloc[-1]["SMA50"]
    sma30 = f.iloc[-1]["SMA30"]
    sma100 = f.iloc[-1]["SMA100"]
    sma200 = f.iloc[-1]["SMA200"]
    if sma50 > sma100 and sma100 > sma200:
        print("Long condition, finding entry")
        if close < sma30 and close > sma50:
            print("long position confirmed")
            print(sma30)
            print(close)
            return "long"
    elif sma50 < sma100 and sma100 < sma200:
        print("short condition, finding entry")
        if close > sma30 and close < sma50:
            print("short condition confirmed")          
            print(sma30)
            print(close)
            return "short"
    else:
        return  None

