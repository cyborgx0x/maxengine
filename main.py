from f_engine import Engine, get_data, FakeServer, TimeMachine, SingleLine

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
