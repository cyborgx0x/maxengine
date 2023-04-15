import time
import datetime
from threading import Thread, Lock
from typing import Any


class Config():
    speed = 100

class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    """

    _instances = {}

    _lock: Lock = Lock()
    """
    We now have a lock object that will be used to synchronize threads during
    first access to the Singleton.
    """

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        # Now, imagine that the program has just been launched. Since there's no
        # Singleton instance yet, multiple threads can simultaneously pass the
        # previous conditional and reach this point almost at the same time. The
        # first of them will acquire lock and will proceed further, while the
        # rest will wait here.
        with cls._lock:
            # The first thread to acquire the lock, reaches this conditional,
            # goes inside and creates the Singleton instance. Once it leaves the
            # lock block, a thread that might have been waiting for the lock
            # release may then enter this section. But since the Singleton field
            # is already initialized, the thread won't create a new object.
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]

class TimeMachine(metaclass=SingletonMeta):
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
