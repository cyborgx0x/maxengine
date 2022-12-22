from .symbol import Symbol
class Signal(object):
    def __init__(self, data) -> None:
        self._data = data
        self.signal = True
    def get_signal(self):
        return {
            "name": symbol,
            "order_type": "sell",
            "price": fif_dt.price,
        }

class Trend_Following(Signal):
    def get_signal(self):
       return super().get_signal()


def get_signal(symbol):
  daily_dt = Symbol(symbol, "2Y", "1D")
  hour_dt = Symbol(symbol, "20D", "60m")
  fif_dt = Symbol(symbol, "5D", "15m")
  buy =  daily_dt.uptrend and fif_dt.uptrend and fif_dt.buy
  sell = daily_dt.downtrend and fif_dt.downtrend and fif_dt.sell
  if buy:
    return {
        "name": symbol,
        "signal": "buy",
        "price": fif_dt.price,
    }
  elif sell:
    return {
        "name": symbol,
        "signal": "sell",
        "price": fif_dt.price,
    }
  else:
    return {
        "name": symbol,
        "signal": "none",
        "price": fif_dt.price,
    }
