from f_engine import *

def main(symbol):
    time_machine = TimeMachine()
    start_date = "2022-01-01"
    end_date = "2023-01-01"
    
    time_machine.begin_time = start_date
    time_machine.end_time = end_date

    server = FakeServer()
    server.data.get_data(symbol, "2Y","1D")
    engine = Engine()

    time_machine.set_speed(100)
    time_machine.server = server

    while time_machine.back_in_time():
        # Test Price and Time
        price = server.get_price()
        server_time = server.time.current_time
        engine_time = engine.time.current_time
        print(f"current price: {price}")
        print(f"server time: {server_time}")
        print(f"engine time: {engine_time}")
        
        engine.connect(server)
        strategy = SingleLine(symbol)
        engine.signal_set.append(strategy)
        engine.execute_trade()
        server.execute_trade()
        engine.signal_set.clear()  
        del strategy
        
        # engine.connect()
        # engine.execute_trade()

    print(server.order)


if __name__=="__main__":
    symbol = "GBPUSD=X"
    main(symbol=symbol)
    