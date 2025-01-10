from api.oanda_api import OandaApi
from infrastructure.instrument_collection import instrumentCollection
from simulation.ma_cross import run_ma_sim
from dateutil import parser
from infrastructure.collect_data import run_collection
from simulation.ema_macd_mp import run_ema_macd
from api.stream_prices import stream_prices

if __name__ == "__main__":
    api = OandaApi()

    # dfr = parser.parse("2021-04-21T01:00:00Z")
    # dto = parser.parse("2021-04-28T16:00:00Z")

    # df_candles = api.get_candles_df("EUR_USD", granularity="H1", date_f=dfr, date_t=dto)

    # print(df_candles.head())
    # print()
    # print(df_candles.tail())

    # print(api.fetch_candles("EUR_USD", granularity="D", price="MB"))

    # data = api.get_account_summary()
    # print(data)

    # instrumentCollection.CreateFile(api.get_account_instruments(), "./data")
    instrumentCollection.LoadInstruments("./data")
    # instrumentCollection.PrintInstruments()

    # run_ma_sim(curr_list=["EUR", "USD", "GBP", "JPY", "AUD", "CAD"])

    # run_collection(instrumentCollection, api)

    # run_ma_sim()
    # stream_prices(['GBP_JPY', 'AUD_NZD'])
    trade_id = api.place_trade(
    pair_name='EUR_USD',
    units=1.0,
    direction=1,  # 1 for BUY, -1 for SELL
    stop_loss=1.0,  # Just to see if it works (not realistic numbers!)
    take_profit=2.0
    )

    print("Trade ID is:", trade_id)
    

