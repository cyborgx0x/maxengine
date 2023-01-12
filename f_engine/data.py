import matplotlib.pyplot as plt
import yfinance as yf
import os.path
import pandas as pd
import datetime
import os
from pandas import DataFrame


def check_time(self):
    if os.path.exists(self.file_name):
        mtime = os.path.getmtime(self.file_name)
        mtime = datetime.datetime.fromtimestamp(mtime)
        if datetime.datetime.now() - mtime > datetime.timedelta(minutes=15):
            os.remove(self.file_name)
            os.remove(self.graph)
            print("Removing old Data")


class Pair():
    def __init__(self, name: str) -> None:
        self.name = name
        self.get_data()

    def get_data(self, symbol: str, period: str, interval: str):
        data = yf.download(tickers=symbol, period=period, interval=interval)
        self.data = data

    def get_current_price(self):
        pass


def get_data(symbol: str, period: str, interval: str) -> DataFrame:

    '''
    Take symbol name, period, interval and return a Dataframe

    This function originally get data from yfinance. 
    Its can be extended later

    '''
    data = yf.download(tickers=symbol, period=period, interval=interval)
    return data