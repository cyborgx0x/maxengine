from f_engine import MT5Account, Engine, SingleLine, multi_timeframe_sma
from dotenv import load_dotenv
import time
import os
import MetaTrader5 as mt
import datetime
load_dotenv()

def simple_strategy(engine: Engine, instrument: str) -> None:
    instrument = instrument
    engine.signal_set.append(SingleLine(instrument))
    engine.execute_trade(mt5=True)
    engine.signal_set.clear()

mt5 = MT5Account()
mt5.account_number = os.getenv("account_number")
mt5.password = os.getenv("password")
mt5.server = os.getenv("server")
mt5.start()
mt5.login()
engine = Engine()
engine.connect_mt5(mt5=mt5)

all_pair = mt5.get_all_pair()

for i in all_pair:
    simple_strategy(engine, i)


def complex_strategy(engine: Engine, instrument:str)->None:
    m15_price = mt5.get_history_price(instrument, mt.TIMEFRAME_M15, datetime.datetime.fromisoformat("2018-01-01"), datetime.datetime.now())
    h1_price = mt5.get_history_price(instrument, mt.TIMEFRAME_H1, datetime.datetime.fromisoformat("2018-01-01"), datetime.datetime.now())
    d1_price = mt5.get_history_price(instrument, mt.TIMEFRAME_D1, datetime.datetime.fromisoformat("2018-01-01"), datetime.datetime.now())
    result = multi_timeframe_sma(m15_price, h1_price, d1_price)
    print(result)