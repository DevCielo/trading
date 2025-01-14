import json
from models.trade_settings import TradeSettings


class TradeSettingsCollection:

    FILENAME = "settings.json"


    def __init__(self):
        self.trade_settings_dict = {}
        self.granularity = "H1"
        self.trade_risk = 1.0


    def load_trade_settings(self):
        self.trade_settings_dict = {}
        fileName = f"./stream_bot/{self.FILENAME}"
        with open(fileName, "r") as f:
            data = json.loads(f.read())
            self.granularity = data['granularity']  
            self.trade_risk = data['trade_risk']  
            for pair, pair_settings in data['pairs'].items():
                self.trade_settings_dict[pair] = TradeSettings(pair_settings, pair)


    def print_collection(self):
        print(f"Granularity: {self.granularity}")
        print(f"Trade Risk: {self.trade_risk}")
        [print(f"{k}: {v}") for k, v in self.trade_settings_dict.items()]


    def pair_list(self )->list:
        return list(self.trade_settings_dict.keys())
    

    def get_trade_settings(self, pair:str)->TradeSettings:
        return self.trade_settings_dict[pair]



tradeSettingsCollection = TradeSettingsCollection()
