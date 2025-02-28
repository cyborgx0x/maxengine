'''
This Module Should Provide full support to work with Large Amount Of Data

Data can contain millions of record.

'''

import matplotlib.pyplot as plt
import yfinance as yf
import os.path
import pandas as pd
import datetime
import os
from pandas import DataFrame
import MetaTrader5 as mt
from .time_machine import TimeMachine

def check_time(self):
    if os.path.exists(self.file_name):
        mtime = os.path.getmtime(self.file_name)
        mtime = datetime.datetime.fromtimestamp(mtime)
        if datetime.datetime.now() - mtime > datetime.timedelta(minutes=15):
            os.remove(self.file_name)
            os.remove(self.graph)


class Data():
    '''
    provide the way to manage data from various sources

    '''
    time = TimeMachine()
    def __init__(self) -> None:
        pass
    def get_data(self, symbol: str, period: str, interval: str):
        data:DataFrame = yf.download(tickers=symbol, period=period, interval=interval)
        data.rename(columns={'Close':'close'}, inplace=True)
        self.yahoo_data = data
        print(data)
    def get_mt_data(self, *args, **kwargs):

        history = mt.copy_rates_range(*args, **kwargs)
        history_frame = pd.DataFrame(history)
        self.full_data = history_frame
        return history_frame
    def get_mt_data_v2(self,symbol, timeframe):
        self.m15 = self.time.current_time - datetime.timedelta(5)
        self.h1 = self.time.current_time - datetime.timedelta(20)
        self.d1 = self.time.current_time - datetime.timedelta(300)
        start_time = self.__getattribute__(timeframe)
        end_time = self.time.current_time
        data = mt.copy_rates_range(symbol, mt.TIMEFRAME_M15, start_time, end_time)
        print(data)
        return data

    def get_data_v2(self, symbol, timeframe):
        '''
        get the data outside of mt5
        '''
        return None


def get_data(symbol: str, period: str, interval: str) -> DataFrame:

    '''
    Take symbol name, period, interval and return a Dataframe

    This function originally get data from yfinance. 
    Its can be extended later

    '''
    data = yf.download(tickers=symbol, period=period, interval=interval)
    return data

