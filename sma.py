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