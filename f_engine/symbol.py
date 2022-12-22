import matplotlib.pyplot as plt
import yfinance as yf
import os.path
import pandas as pd
import datetime
import os


class Symbol():
  def __init__(self, symbol, period, interval):
    self.symbol = symbol
    self.period = period
    self.interval =  interval
    self.file_name = self.symbol + self.period + self.interval + ".csv"
    self.graph = "app/static/" + self.symbol + self.period + self.interval + ".jpg"
    self.graph_abs = self.symbol + self.period + self.interval + ".jpg"
    self.check_time()
    self.data = self.get_data()
    self.trans_data = self.transfer(self.data)
    self.uptrend = False
    self.downtrend = False
    self.buy = False
    self.sell = False
    self.price = 0
    self.trend(self.trans_data)
    self.plot()
  def transfer(self, dataframe):
    f =  dataframe[["Close"]].copy()
    
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
    if os.path.exists(self.graph):
      pass
    else:
      plt.figure(num=self.graph)
      plt.title = self.symbol + self.interval
      plt.plot(self.trans_data)
      plt.savefig(self.graph)
  def get_data(self):
    if os.path.exists(self.file_name):
      data = pd.read_csv(self.file_name)
      return data
    else:
      data = yf.download(tickers = self.symbol, period = self.period, interval = self.interval)
      data.to_csv(self.file_name)
      return data
  def check_time(self):
    if os.path.exists(self.file_name):
      mtime = os.path.getmtime(self.file_name)
      mtime = datetime.datetime.fromtimestamp(mtime)
      if datetime.datetime.now() - mtime > datetime.timedelta(minutes=15):
          os.remove(self.file_name)
          os.remove(self.graph)
          print("Removing old Data")


