# python main.py to run
import json
import requests
import os
import threading
import pandas as pd
from timeit import default_timer as timer
import constants.defs as defs
from models.live_api_price import LiveApiPrice
from infrastructure.log_wrapper import LogWrapper
from streaming.stream_base import StreamBase

from dotenv import load_dotenv

load_dotenv()

STREAM_URL = f"https://stream-fxpractice.oanda.com/v3"

API_KEY = os.getenv("API_KEY")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")
OANDA_URL = os.getenv("OANDA_URL")

print(f"API_KEY: {API_KEY}")
print(f"ACCOUNT_ID: {ACCOUNT_ID}")
print(f"OANDA_URL: {OANDA_URL}")
class PriceStreamer(StreamBase):

    LOG_FREQ = 20

    def __init__(self, shared_prices, price_lock: threading.Lock, price_events):
        """
        Initializes the PriceStreamer thread.

        Args:
            shared_prices (dict): A dictionary containing the shared prices data, 
                where new prices will be placed for processing.
            price_lock (threading.Lock): A lock to ensure thread-safe operations 
                on the shared prices.
            price_events (dict): A dictionary of events that trigger when new 
                prices are received.

        Attributes:
            pairs_list (dict_keys): The list of currency pairs being monitored.
            price_lock (threading.Lock): The lock object for thread-safe access 
                to shared prices.
            price_events (dict): The events associated with each currency pair 
                for notifying price updates.
            shared_prices (dict): The shared prices data structure.
            log (LogWrapper): Logger for the PriceStreamer operations.
        """
        super().__init__(shared_prices, price_lock, price_events, "PriceStreamer")
        self.pairs_list = shared_prices.keys()
        print(self.pairs_list)

    def fire_new_price_event(self, instrument):
        if self.price_events[instrument].is_set() == False:
            self.price_events[instrument].set()

    def update_live_price(self, live_price: LiveApiPrice):
        """
        Updates the shared prices data structure with a new price. 
        Locks it so only one thread can access shared_prices at a time.

        Args:
            live_price (LiveApiPrice): The new price to be added to the shared prices.

        Notes:
            This method is thread-safe.
        """
        try:
            self.price_lock.acquire()
            self.shared_prices[live_price.instrument] = live_price
            self.fire_new_price_event(live_price.instrument)

        except Exception as error:
            self.log_message(f"Exception: {error}", error=True)
        finally:
            self.price_lock.release()

    def log_data(self):
        self.log_message("")
        self.log_message(f"\n{pd.DataFrame.from_dict([v.get_dict() for _, v in self.shared_prices.items()])}")

    def run(self):

        # Make the first logging of prices after 10 seconds
        start = timer() - PriceStreamer.LOG_FREQ + 10

        params = dict(
            instruments=','.join(self.pairs_list)
        )

        url = f"{STREAM_URL}/accounts/{ACCOUNT_ID}/pricing/stream"

        resp = requests.get(url, params=params, headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }, stream=True)

        for price in resp.iter_lines():
            if price:
                decoded_price = json.loads(price.decode('utf-8'))
                if 'type' in decoded_price and decoded_price['type'] == 'PRICE':
                    # Processing
                    self.update_live_price(LiveApiPrice(decoded_price))
                    # More than 60 secs have passed
                    # print(LiveApiPrice(decoded_price).get_dict())
                    if timer() - start > PriceStreamer.LOG_FREQ:
                        print(LiveApiPrice(decoded_price).get_dict())
                        self.log_data()
                        start = timer()
                    