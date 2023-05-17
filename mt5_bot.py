from f_engine import MT5Account, Engine, SingleLine, MultiTimeframeTrendFollowing
import configurations
from dotenv import load_dotenv
import os
load_dotenv()

def simple_strategy(engine: Engine, instrument: str) -> None:
    engine.signal_set.append(SingleLine(symbol=instrument))
    engine.execute_trade(mt5=True)
    engine.signal_set.clear()

mt5 = MT5Account()
mt5.account_number = configurations.MT5_ACCOUNT_NUMBER
mt5.password = configurations.MT5_PASSWORD
mt5.server = configurations.MT5_PASSWORD
mt5.start()
mt5.login()
engine = Engine()
engine.connect_mt5(mt5=mt5)
def complex_strategy(engine: Engine, instrument:str)->None:
    engine.signal_set.append(MultiTimeframeTrendFollowing(symbol=instrument))
    engine.execute_trade(mt5=True)
    engine.signal_set.clear()

pairs = []
trading_pair = []

for pair in pairs:
    if pair.spread > 20:
        continue
    else:
        trading_pair.append(pair)

class Executor():
    position = []
    
    @property
    def pnl(self):
        return self.calculate_pnl()

class Server():
    exness = ""


class PairCondition():
    spread = 0
    
    
    def __init__(self) -> None:
        pass
    
    @property
    def volatility(self):
        return 
    
    @property
    def volatility_threshold(self):
        '''
        Update the threshold calculation here. 
        By taking the volatility range, the function can return the threshold.
        Therefore the agent can detemine the quality of current environment
        '''
        pass

    @property
    def confident_score(self):
        return self.calculate_confident()
    

    @staticmethod
    def calculate_confident(self):
        pass
    
    @property
    def is_ok(self, spread, volatility) -> bool:
        if self.spread > 20:
            return False
        if self.volatility > self.volatility_threshold:
            return False
        
class Pair():
    condition = PairCondition()
    
class MarketCondition():
    @property
    def is_ok(self):
        pass

all_pair = mt5.get_all_pair()

for i in all_pair:
    complex_strategy(engine, i)

def check_condition():
    '''
    Combine all criteria and return if the condition is good for trading or not.
    '''

    market = MarketCondition()
    pair = Pair()
    condition = []
    condition.append(
        pair.condition.is_ok,
        market.is_ok
    )
    should_i = bool(condition)
    return should_i



