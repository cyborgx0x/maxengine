import MetaTrader5 as mt
class Order():
    '''
    mimic the order that client send to the server

    this should be compatible with mt5 or other famous trading system.
    '''
    action = ""
    symbol = ""
    volume = 1000
    mt_type = -1
    price = 0
    sl = 0
    tp = 0
    deviation = 20
    magic = 888888
    comment = "F Engine Automate Trading System"
    type_time = ""
    type_filling = ""

    def __init__(self, *args, **kwargs) -> None:
        # self.__setattr__(*args, **kwargs)
        pass

    def __repr__(self) -> str:
        # self.get_mt5_order()
        return f"{self.mt_type} for {self.symbol} at price {self.price} "

    def get_mt5_order(self) -> None:
        point = mt.symbol_info(self.symbol).point
        if self.mt_type == "buy":
            self.price = mt.symbol_info_tick(self.symbol).ask
            mt_type = mt.ORDER_TYPE_BUY
            sl = self.price - 1000 * point
            tp = self.price + 1000 * point
        else:
            mt_type = mt.ORDER_TYPE_SELL
            self.price = mt.symbol_info_tick(self.symbol).bid
            sl = self.price + 1000 * point
            tp = self.price - 1000 * point
        request =  {
            "action": mt.TRADE_ACTION_DEAL,
            "symbol": "BATUSDm",
            "volume": 0.1,
            "type": mt_type,
            "deviation": 20,
            "magic": 888666,
            "comment": "TEST",
            "type_time": mt.ORDER_TIME_GTC,
            "type_filling": mt.ORDER_FILLING_IOC,
        }
        print(self.mt_type)
        print(request)
        return request

# o.__dict__["func"] = 0
