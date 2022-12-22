import matplotlib.pyplot as plt
import yfinance as yf
import os.path
import pandas as pd
import datetime
import os

def get_data(symbol, period, interval):
      data = yf.download(tickers = symbol, period = period, interval = interval)
      return data

def check_time(self):
    if os.path.exists(self.file_name):
      mtime = os.path.getmtime(self.file_name)
      mtime = datetime.datetime.fromtimestamp(mtime)
      if datetime.datetime.now() - mtime > datetime.timedelta(minutes=15):
          os.remove(self.file_name)
          os.remove(self.graph)
          print("Removing old Data")

