import time
import datetime

class TimeMachine():
    def __init__(self):
        self.config = {}
        self.begin_time = datetime.date.fromisoformat("2022-01-01")
        self.end_time = datetime.date.fromisoformat("2023-01-01")
        
    def back_in_time(self):
        self.run()
        if self.current_time == self.end_time:
            self.status = False
        else:
            self.status = True
        return self.status
    def register(self, *args, **kwargs):
        if args:
            for i in args:
                print(i)
        if kwargs:
            for k, value in kwargs.items():
                self.data[k]=value
    def set_begin(self, begin) -> None:
        self.begin_time = datetime.date.fromisoformat(begin)
        self.current_time = self.begin_time
    def set_end(self, end) -> None:
        self.end_time = datetime.date.fromisoformat(end)
    def run(self):
        self.status = True
        time.sleep(2/self.config["speed"])
        self.current_time = self.current_time + datetime.timedelta(days=1)
    def event_register(self) -> None:
        return 0
    def set_speed(self, par) -> None:
        self.config["speed"] = par

