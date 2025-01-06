import requests
import pandas as pd
from dotenv import load_dotenv
import os
from dateutil import parser
from datetime import datetime as dt

load_dotenv()

API_KEY = os.getenv("API_KEY")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")
OANDA_URL = os.getenv("OANDA_URL")

class OandaApi:
    def __init__(self):
        self.session = requests.Session()

        self.session.headers.update({
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        })
    
    '''
    Makes HTTP requests to the oanda api. Constructs full API URL, sends request and checks response status.
    Returns True if the response code is 200. 

    url: the endpoint of the request
    verb: get, post, put, delete
    code: Expected HTTP response code
    params: GET params
    data: POST data
    headers: POST headers
    '''
    def make_request(self, url, verb='get', code=200, params=None, data=None, headers=None):
        full_url = f"{OANDA_URL}/{url}"
        try:
            response = None
            if verb == 'get':
                response = self.session.get(full_url, params=params, data=data, headers=headers)
            
            if response == None:
                return False, {'error': 'verb not found'}

            if response.status_code == code:
                return True, response.json()
            else:
                return False, response.json()

        except Exception as error:
            return False, {'Exception': error}

    '''
    Fetches account-related-data
    Constructs the URL, sends the request and checks the response
    '''
    def get_account_ep(self, ep, data_key):
        url = f"accounts/{ACCOUNT_ID}/{ep}"
        ok, data = self.make_request(url)

        if ok and data_key in data:
            return data[data_key]
        else:
            print("ERROR get_account_ep()", data)
            return None
    
    # Retrieves account summary
    def get_account_summary(self):
        return self.get_account_ep("summary", "account")

    # Retrieves the list of tradable instruments
    def get_account_instruments(self):
        return self.get_account_ep("instruments", "instruments")

    '''
    Fetches historical price data (candles) for given currency pair

    pair_name: currency pair ("EUR_USD")
    count: number of candles to fetch
    granularity: candle size (H1, M1, M5, M15, M30, H4, H8, H12, H1)
    price: candle type (MBA, MID, BID, ASK)
    date_f, date_t: Optional date range for candles
    '''
    def fetch_candles(self, pair_name, count=10, granularity="H1", price="MBA", date_f=None, date_t=None):
        url = f"instruments/{pair_name}/candles"
        params = dict(
            granularity = granularity,
            price = price
        )

        # If date_f and date_t are provided, it formats them, otherwise it uses count to specify number of candles
        if date_f is not None and date_t is not None:
            date_format = "%Y-%m-%dT%H:%M:%SZ"
            params['from'] = dt.strftime(date_f, date_format)
            params['to'] = dt.strftime(date_t, date_format)
        else:
            params["count"] = count

        ok, data = self.make_request(url, params=params)
        
        if ok and 'candles' in data:
            return data['candles']
        else:
            print("ERROR fetch_candles()", params, data)
            return None

    def get_candles_df(self, pair_name, **kwargs):
        data = self.fetch_candles(pair_name, **kwargs)
        
        if data is None:
            return None
        if len(data) == 0:
            return pd.DataFrame()

        prices = ['mid', 'bid', 'ask']
        ohlc = ['o', 'h', 'l', 'c']

        final_data = []
        for candle in data:
            if candle['complete'] == False:
                continue

            new_dict = {}
            new_dict['time'] = parser.parse(candle['time'])
            new_dict['volumne'] = candle['volume']
            for p in prices:
                if p in candle:
                    for o in ohlc:
                        new_dict[f"{p}_{o}"] = float(candle[p][o])

            final_data.append(new_dict)

        df = pd.DataFrame.from_dict(final_data)
        return df