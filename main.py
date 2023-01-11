from f_engine import Engine, Signal, TripleMA, get_data

class Trend_Following(Signal):
    def trend(self):
        daily_dt = TripleMA(self._data.get("daily"))
        hour_dt = TripleMA(self._data.get("hourly"))
        fif_dt = TripleMA(self._data.get("fifteen"))
        self.price = daily_dt.price
        if daily_dt.get_result() == "uptrend" and hour_dt.get_result() == "uptrend":
            self.order_type = "buy"
        if daily_dt.get_result() == "downtrend" and hour_dt.get_result() == "downtrend":
            self.order_type = "sell"
        

if __name__=="__main__":
    symbol = "GBPUSD=X"
    daily_data = get_data(symbol = symbol,period = "2Y", interval = "1D")
    hour_data = get_data(symbol, "20D", "60m")
    fifteen_data = get_data(symbol, "5D", "15m")
    data = {
        "symbol": symbol,
        "daily": daily_data,
        "daily": hour_data,
        "fifteen": fifteen_data
    }
    engine = Engine(data)
    engine.execute_trade(Trend_Following(data))

    