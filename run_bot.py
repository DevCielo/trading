# from bot.bot import Bot
from stream_bot.stream_bot import run_bot
from infrastructure.instrument_collection import instrumentCollection

if __name__ == "__main__":
    instrumentCollection.LoadInstruments("./data")
    #b = Bot()
    #b.run()
    run_bot()