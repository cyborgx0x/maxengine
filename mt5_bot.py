from f_engine import MT5Account, Engine, SingleLine, MultiTimeframeTrendFollowing
from configurations import *

def simple_strategy(engine: Engine, instrument: str) -> None:
    engine.signal_set.append(SingleLine(symbol=instrument))
    engine.execute_trade(mt5=True)
    engine.signal_set.clear()

mt5 = MT5Account()
mt5.account_number = MT5_ACCOUNT_NUMBER
mt5.password = MT5_PASSWORD
mt5.server = MT5_SERVER
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
#Trading logic
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
        
    def __repr__(self) -> str:
        return f'''
        Current Pair Condition:
        {self.is_ok}
        With the following confident score:
        {self.confident_score}
        '''
        
class Pair():
    condition = PairCondition()
    
class MarketCondition():
    
    @property
    def is_ok(self):
        return None

    @property
    def confident_score(self):
        return self.calculate_confident()

    def calculate_confident(self):
        return None

    @property
    def market_score(self):
        pass

    def __repr__(self) -> str:
        return f'''
        Current Market Condition: {self.is_ok}
        Confident Score: {self.confident_score}
        '''

all_pair = mt5.get_all_pair()

for pair in all_pair:
    complex_strategy(engine, pair)

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
    print(market)

    should_i = bool(condition)
    return should_i

'''
After all the analysis is the capital management process
We have to make sure to check the risk management even with 99.99% percent confident score of analysis
The following code will implement the 5% rule when it come to risk management. 
But even with tight stop and 5% rule, it can not protect your capital from extreme events,
In these kind of event, the lack of liquidity will kill your position in the disfavor. 
Make sure to locate your capital several business that you know well so you can recover later.
'''

class RiskControl():
    available_capital = 0
    margin_rate = 0
    current_position = []

    @property
    def risk_score(self):
        return self.calculate_risk_score()
    
    def calculate_risk_score(self):
        pass

    @property
    def available_capital(self):
        return self.calculate_available_capital()
    

    