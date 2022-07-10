import yfinance as yf
import os.path
import pandas as pd

class Symbol():
  def __init__(self, dataframe):
    self.data = dataframe
    self.trans_data = self.transfer(self.data)
    self.uptrend = False
    self.downtrend = False
    self.buy = False
    self.sell = False
    self.price = 0
    self.trend(self.trans_data)
  def transfer(self, dataframe):
    f =  dataframe["Close"].to_frame()
    f["SMA30"] = f["Close"].rolling(30).mean()
    f["SMA50"] = f["Close"].rolling(50).mean()
    f["SMA100"] = f["Close"].rolling(100).mean()
    f["SMA200"] = f["Close"].rolling(200).mean()
    f.dropna(inplace = True)
    return f
  def trend(self, trans_data):
    last_price = trans_data.tail(1)
    self.uptrend = last_price["SMA50"].item() > last_price["SMA100"].item() and last_price["SMA100"].item() > last_price["SMA200"].item()
    self.downtrend = last_price["SMA50"].item() < last_price["SMA100"].item() and last_price["SMA100"].item() > last_price["SMA200"].item()
    self.price = last_price["Close"].item()
    self.buy = self.price > last_price["SMA200"].item() and self.price < last_price["SMA50"].item() 
    self.sell = self.price < last_price["SMA200"].item() and self.price > last_price["SMA50"].item()
  def plot(self):
    self.trans_data.plot()

def cached(symbol, period, interval):
  file_name = symbol + period + interval + ".csv"
  if os.path.exists(file_name):
    data = pd.read_csv(file_name)
    return data
  else:
    data = yf.download(tickers = symbol, period = period, interval = interval)
    data.to_csv(file_name)
    return data

def get_signal(symbol):
  daily = cached(symbol,"2Y", "1D")
  hour = cached(symbol,"20D", "60m")
  fifteen = cached(symbol,"5D", "15m")
  daily_dt = Symbol(daily)
  hour_dt = Symbol(hour)
  fif_dt = Symbol(fifteen)
  buy =  daily_dt.uptrend and fif_dt.uptrend and fif_dt.buy
  sell = daily_dt.downtrend and fif_dt.downtrend and fif_dt.sell
  if buy:
    return {
        "name": symbol,
        "signal": "buy",
        "price": fif_dt.price,
    }
  elif sell:
    return {
        "name": symbol,
        "signal": "sell",
        "price": fif_dt.price,
    }
  else:
    return {
        "name": symbol,
        "signal": "none",
        "price": fif_dt.price,
    }