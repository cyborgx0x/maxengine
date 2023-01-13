import time
import datetime


class Config():
    speed = 100


class TimeMachine():
    _config = Config()

    def __init__(self):

        self._begin_time = "2022-01-01"
        self._end_time = "2023-01-01"

    def back_in_time(self) -> None:
        self.run()
        if self.current_time == self.end_time:
            self.status = False
        else:
            self.status = True
        return self.status

    def run(self):
        self.status = True
        time.sleep(2/self.config.speed)
        self.current_time = self.current_time + datetime.timedelta(days=1)

    def register(self, *args, **kwargs) -> None:
        """
        Register a component to be call later on
        """
        self.__setattr__(*args, **kwargs)

    @property
    def end_time(self) -> bool:
        return self._end_time

    @end_time.setter
    def end_time(self, end) -> bool:
        self._end_time = datetime.date.fromisoformat(end)

    def event_register(self) -> None:
        '''
        let the agent interact with each other
        '''
        pass

    def set_speed(self, par) -> None:
        self._config.speed = 1000

    @property
    def begin_time(self) -> None:
        return self._begin_time

    @begin_time.setter
    def begin_time(self, begin) -> None:
        print(type(begin))
        self._begin_time = datetime.date.fromisoformat(begin)
        self.current_time = self.begin_time

    @property
    def config(self) -> None:
        return self._config

    @config.setter
    def config(self, key) -> None:
        self.config.__dic__[key.__name__] = key
