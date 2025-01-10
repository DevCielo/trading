from api.oanda_api import OandaApi
from infrastructure.instrument_collection import instrumentCollection
from models.candle_timing import CandleTiming
import time 
from bot.trade_risk_calculator import get_trade_units
import constants.defs as defs

def lm(msg, pair):
    print(msg, pair)

if __name__ == "__main__":
    api = OandaApi()
    instrumentCollection.LoadInstruments("./data")
    #trade_id = api.place_trade("EUR_USD", 100, 1)
    #print("opened", trade_id)
    #time.sleep(10)
    #print(f"closing {trade_id}", api.close_trade(trade_id))
    # [api.close_trade(x.id) for x in api.get_open_trades()]
    #dd = api.last_complete_candle("EUR_USD", granularity="M5")
    #print(CandleTiming(dd))
    # print(api.get_prices(["GBP_JPY", "AUD_NZD"]))

    # print(get_trade_units(api, "EUR_USD", defs.BUY, 0.0055, 30, lm))