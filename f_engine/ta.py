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


def compute_sma(history_price):
    f = history_price["close"].to_frame()
    f["SMA30"] = f["close"].rolling(30).mean()
    f["SMA50"] = f["close"].rolling(50).mean()
    f["SMA100"] = f["close"].rolling(100).mean()
    f["SMA200"] = f["close"].rolling(200).mean()
    f.dropna(inplace = True)
    return f
    
def multi_timeframe_sma(m15_price, h1_price, d1_price):
    d1_sma = compute_sma(d1_price)
    h1_sma = compute_sma(h1_price)
    m15_sma = compute_sma(m15_price)
    last_d1 = d1_sma.iloc[-1]
    last_h1 = h1_sma.iloc[-1]
    last_m15 = m15_sma.iloc[-1]
    d1_long_condition = last_d1["SMA50"] > last_d1["SMA100"] and last_d1["SMA100"] > last_d1["SMA200"] 
    h1_long_condition = last_h1["SMA50"] > last_h1["SMA100"] and last_h1["SMA100"] > last_h1["SMA200"] 
    m15_long_condition = last_m15["SMA50"] > last_m15["close"] and last_m15["close"] > last_m15["SMA200"] 
    d1_short_condition = last_d1["SMA50"] < last_d1["SMA100"] and last_d1["SMA100"] < last_d1["SMA200"] 
    h1_short_condition = last_h1["SMA50"] < last_h1["SMA100"] and last_h1["SMA100"] < last_h1["SMA200"] 
    m15_short_condition = last_m15["SMA50"] < last_m15["close"] and last_m15["close"] < last_m15["SMA200"] 
    if d1_long_condition and m15_long_condition:
        print("strictly long condition met!")
        return "long"
    elif d1_short_condition  and m15_short_condition:
        print("strictly short condition met!")
        return "short"
    else:
        print("nothing found")
    
    



