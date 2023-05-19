from dotenv import load_dotenv
from f_engine import MT5Account
import os
import MetaTrader5 as mt
import pandas as pd
import datetime
load_dotenv()

mt5 = MT5Account()
mt5.account_number = os.getenv("account_number")
mt5.password = os.getenv("password")
mt5.server = os.getenv("server")
mt5.start()
mt5.login()

data = mt.copy_rates_range("GBPUSDm", mt.TIMEFRAME_M5, datetime.datetime(2018,8,30), datetime.datetime(2018,12,1))
df = pd.DataFrame(data)
print(df)
