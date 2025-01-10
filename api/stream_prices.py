import json
import requests
import os

import constants.defs as defs

STREAM_URL = f"https://stream-fxpractice.oanda.com/v3"

API_KEY = os.getenv("API_KEY")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")
OANDA_URL = os.getenv("OANDA_URL")

'''
For real time stream pricing (connects to OANDA's pricing stream and continuously listens for price updates)
'''
def stream_prices(pairs_list):
    params = dict(
        instruments=','.join(pairs_list)
    )

    url = f"{STREAM_URL}/accounts/{ACCOUNT_ID}/pricing/stream"

    resp = requests.get(url, params=params, headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }, stream=True)

    for price in resp.iter_lines():
        if price:
            decoded_price = json.loads(price.decode('utf-8'))
            print(decoded_price)
            print()