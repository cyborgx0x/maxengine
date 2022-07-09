import yfinance as yf

class Symbol():
  def __init__(self, dataframe):
    self.data = dataframe
    self.trans_data = self.transfer(self.data)
    self.uptrend = False
    self.downtrend = False
    self.buy = False
    self.sell = False
    self.price = 0
    self.trend(self.trans_data)
  def transfer(self, dataframe):
    f =  dataframe["Close"].to_frame()
    f["SMA30"] = f["Close"].rolling(30).mean()
    f["SMA50"] = f["Close"].rolling(50).mean()
    f["SMA100"] = f["Close"].rolling(100).mean()
    f["SMA200"] = f["Close"].rolling(200).mean()
    f.dropna(inplace = True)
    return f
  def trend(self, trans_data):
    last_price = trans_data.tail(1)
    self.uptrend = last_price["SMA50"].item() > last_price["SMA100"].item() and last_price["SMA100"].item() > last_price["SMA200"].item()
    self.downtrend = last_price["SMA50"].item() < last_price["SMA100"].item() and last_price["SMA100"].item() > last_price["SMA200"].item()
    self.price = last_price["Close"].item()
    self.buy = self.price > last_price["SMA200"].item() and self.price < last_price["SMA50"].item() 
    self.sell = self.price < last_price["SMA200"].item() and self.price > last_price["SMA50"].item()
  def plot(self):
    self.trans_data.plot()

def get_signal(symbol):
  daily = yf.download(tickers = symbol, period = "2Y", interval = "1D")
  daily
  hour = yf.download(tickers = symbol, period = "20D", interval = "60m")
  hour
  fifteen = yf.download(tickers = symbol, period = "5D", interval = "15m")
  fifteen
  daily_dt = Symbol(daily)
  hour_dt = Symbol(hour)
  fif_dt = Symbol(fifteen)
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