import pandas

class Account():
    def __init__(self, capital:int=0, margin:int=0, currency:str="USD") -> None:
        self.capital = capital
        self.margin = margin
        self.currency = currency

class FakeServer():

    account = Account(1000, 20)
    def __init__(self, ) -> None:
        daily_data = ""
        self.order = []
        pass
    def execute_trade(self) -> None:
        for i in self.order:
            print(i)
        if self.account.margin < 1:
            return "Not enough Capital"
    def get_data(self, start_date, end_date, interval):
        if interval == "1D":
            return self.daily_data.loc[start_date:end_date] 
    def filling_order(self, order):
        self.order.append(order)
    def get_price(self):

        current_row =  self.daily_data[self.time.current_time.isoformat():self.time.current_time.isoformat()].tail(1)
        try:
            return current_row["Close"].item()
        except:
            return None
            
    def get_time(self):
        return self.time.current_time
    