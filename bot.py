from sm import Account
from sma import sma_trend
import time

login = {
    "account_number": 88491719,
    "password": "Thienthan9x",
    "server": "Exness-MT5Real15"
}

demo_account = {
    "account_number": 96267091,
    "password": "Thienthan9x",
    "server": "Exness-MT5Trial6"
}

acc = Account(**demo_account)
acc.start()
acc.login()
all_pair = acc.get_all_pair()
while True:
    for i in all_pair:
        print(i)
        instrument = i
        history_price = acc.get_history_price(instrument)
        price = acc.get_current_price(instrument)
        order_type = sma_trend(history_price)
        if order_type:
            acc.trade(instrument, price, order_type=order_type)
    time.sleep(900)
