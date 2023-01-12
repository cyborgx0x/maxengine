from typing import Dict

class Signal(object):
    def __init__(self, data: Dict) -> None:
        self._data = data
        self.price = ""
        self.order_type = ""
    def get_signal(self):
        self.trend()
        return {
            "symbol": self._data.get("symbol"),
            "order_type": self.order_type,
            "price": self.price,
        }
    def trend(self) -> None:
        pass
