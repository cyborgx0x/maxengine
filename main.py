from f_engine import Engine, Signal, TripleMA, get_data, FakeServer
from time_machine import TimeMachine


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
        
class SingleLine(Signal):
    def trend(self):
        daily_dt = TripleMA(self._data.get("daily"))
        try:
            self.price = daily_dt.price
        except:
            print("No Price")
        if daily_dt.get_result()["result"] == "uptrend":
            self.order_type = "buy"
        if daily_dt.get_result()["result"] == "downtrend":
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

    server = FakeServer()
    server.daily_data=daily_data
    server.hour_data=hour_data
    server.fifteen_data=fifteen_data
    engine = Engine()
    time_machine = TimeMachine()
    start_date = "2022-01-01"
    end_date = "2023-01-01"
    time_machine.set_begin(start_date)
    time_machine.set_end(end_date)
    time_machine.set_speed(100)
    time_machine.data = daily_data
    time_machine.server = server
    server.time = time_machine
    engine.time = time_machine
    while time_machine.back_in_time():
        # Test Price and Time
        price = server.get_price()
        server_time = server.get_time()
        engine_time = engine.get_time()
        print(f"current price: {price}")
        print(f"current time: {server_time}")
        print(f"current time: {engine_time}")
        
        # Get Data from Server

        data = server.get_data(start_date, engine_time, "1D")

        data = {
            "symbol": "GBPUSD=X",
            "daily": data,
        }
        engine.connect(server)

        engine.signal_set.append(SingleLine(data))
        engine.execute_trade()
        server.execute_trade()
        engine.signal_set.clear()  

        # engine.connect()
        # engine.execute_trade()

    print(server.order)
