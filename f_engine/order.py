import MetaTrader5 as mt
class Order():
    '''
    mimic the order that client send to the server

    this should be compatible with mt5 or other famous trading system.
    '''
    action = ""
    symbol = ""
    volume = 1000
    type = -1
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
        return f"{self.type} for {self.symbol} at price {self.price} "

    def get_mt5_order(self) -> None:
        point = mt.symbol_info(self.symbol).point

        if self.type == "buy":
            type = mt.ORDER_TYPE_BUY
            sl = self.price - 1000 * point
            tp = self.price + 1000 * point
        else:
            type = mt.ORDER_TYPE_SELL
            sl = self.price + 1000 * point
            tp = self.price - 1000 * point
        return {
            "action": mt.TRADE_ACTION_DEAL,
            "symbol": self.symbol,
            "volume": 0.1,
            "type": type,
            "price": self.price,
            "sl": sl,
            "tp": tp,
            "deviation": 20,
            "magic": 234300,
            "comment": self.comment,
            "type_time": mt.ORDER_TIME_GTC,
            "type_filling": mt.ORDER_FILLING_IOC,
        }

# o.__dict__["func"] = 0
