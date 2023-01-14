from f_engine import MT5Account, Engine, SingleLine, MultiTimeframeTrendFollowing
from dotenv import load_dotenv
import os
load_dotenv()

def simple_strategy(engine: Engine, instrument: str) -> None:
    engine.signal_set.append(SingleLine(symbol=instrument))
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
def complex_strategy(engine: Engine, instrument:str)->None:
    engine.signal_set.append(MultiTimeframeTrendFollowing(symbol=instrument))
    engine.execute_trade(mt5=True)
    engine.signal_set.clear()
    

all_pair = mt5.get_all_pair()

for i in all_pair:
    complex_strategy(engine, i)

