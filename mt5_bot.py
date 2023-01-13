from f_engine import MT5Account, sma_trend, Engine, SingleLine
from dotenv import load_dotenv
import time
import os
import MetaTrader5 as mt
import datetime
load_dotenv()

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
    print(i)
    instrument = i
    historical_data = mt5.get_history_price(instrument, mt.TIMEFRAME_D1, datetime.datetime.fromisoformat("2018-01-01"), datetime.datetime.now())
    data = {
        "symbol": instrument,
        "daily": historical_data,
    }
    price = mt5.get_current_price(instrument)
    engine.signal_set.append(SingleLine(data))
    engine.execute_trade(mt5=True)
    engine.signal_set.clear()  
    
    # order_type = sma_trend(historical_data)
    # if order_type:
    #     mt5.trade(instrument, price, order_type=order_type)
print(engine.order_list)
