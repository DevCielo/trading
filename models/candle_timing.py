import datetime as dt

class CandleTiming:
    # Candle manager will get the most recent time, and compare it to the last time
    # If newer given time is bigger than the last time it will set is_ready to true
    def __init__(self, last_time):
        self.last_time = last_time
        self.is_ready = False

    def __repr__(self):
        return f"last_candle:{dt.datetime.strftime(self.last_time, '%y-%m-%d %H:%M')} is_ready:{self.is_ready}"
