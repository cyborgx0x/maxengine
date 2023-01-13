from .meta_wrapper import Account
import MetaTrader5 as mt
from .trade_signal import Signal

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
    
    

demo_account = {
    "account_number": 96267091,
    "password": "Thienthan9x",
    "server": "Exness-MT5Trial6"
}

acc = Account(**demo_account)
acc.start()

all_pair = acc.get_all_pair()

for pair in all_pair:
    print(pair)
    try: 
        m15_price = acc.get_history_price(pair, mt.TIMEFRAME_M15, 10)
        h1_price = acc.get_history_price(pair, mt.TIMEFRAME_H1, 60)
        d1_price = acc.get_history_price(pair, mt.TIMEFRAME_D1, 300)
        result = multi_timeframe_sma(m15_price, h1_price, d1_price)
    except:
        print("there is some errors with this pair")