import copy
from queue import Queue
import threading
import datetime as dt

import pytz
from models.live_api_price import LiveApiPrice
from streaming.stream_base import StreamBase


GRANULARITIES = {
    "M1": 1,
    "M5": 5,
    "M15": 15,
    "M30": 30,
    "H1": 60,
}


class PriceProcessor(StreamBase):

    def __init__(self, shared_prices, price_lock: threading.Lock, price_events, 
                 candle_queue: Queue,
                 logname, pair, granularity):
        super().__init__(shared_prices, price_lock, price_events, logname)
        self.pair = pair
        self.candle_queue = candle_queue
        self.granularity = GRANULARITIES[granularity]

        now = dt.datetime.now(pytz.timezone("UTC"))
        self.set_last_candle(now)
        print(f" PriceProcessor : {self.last_complete_candle_time} {now}")
        
    
    def set_last_candle(self, price_time: dt.datetime):
        self.last_complete_candle_time = self.round_time_down(
            price_time - dt.timedelta(minutes=self.granularity)
        )


    def round_time_down(self, round_me: dt.datetime) -> dt.datetime:
        remainder = round_me.minute % self.granularity
        candle_time = dt.datetime(round_me.year, 
							  round_me.month, 
							  round_me.day, 
							  round_me.hour, 
							  round_me.minute - remainder, 
							  tzinfo=pytz.timezone("UTC"))
        return candle_time
    

    def detect_new_candle(self, price: LiveApiPrice):
        old = self.last_complete_candle_time
        self.set_last_candle(price.time)

        if old < self.last_complete_candle_time:
            msg = f"--->>>> {self.pair} New Candle : {self.last_complete_candle_time} {price.time}"
            print(msg)
            self.candle_queue.put(self.last_complete_candle_time)


    def process_price(self):

        try:
            self.price_lock.acquire()
            price: LiveApiPrice = copy.deepcopy(self.shared_prices[self.pair])
            #print(f"PriceProcessor : {price}")
            if price is not None:
                self.detect_new_candle(price)
        except Exception as error:
            self.log_message(f"CRASH : {error}", error=True)
        finally:
            self.price_lock.release()


    def run(self):

        while True:
            self.price_events[self.pair].wait()
            self.process_price()
            self.price_events[self.pair].clear()
