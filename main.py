from api.oanda_api import OandaApi
from infrastructure.instrument_collection import instrumentCollection
from simulation.ma_cross import run_ma_sim
from dateutil import parser
from infrastructure.collect_data import run_collection
from simulation.ema_macd_mp import run_ema_macd
from streaming.streamer import run_streamer
from db.db import DataDB

def db_tests():
    d = DataDB()

    # d.add_one(DataDB.SAMPLE_COLL, dict(age=12, name="fred", eyes='blue'))
    print(d.query_all(DataDB.SAMPLE_COLL, age=13))

if __name__ == "__main__":
    api = OandaApi()
    #instrumentCollection.CreateDB(api.get_account_instruments())
    instrumentCollection.LoadInstrumentsDB()
    print(instrumentCollection.instruments_dict)

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
    #instrumentCollection.LoadInstruments("./data")
    # instrumentCollection.PrintInstruments()

    # run_ma_sim(curr_list=["EUR", "USD", "GBP", "JPY", "AUD", "CAD"])

    # run_collection(instrumentCollection, api)

    # run_ma_sim()
    #run_streamer()
    #d = DataDB()
    #d.test_connection()
    #db_tests()
    

