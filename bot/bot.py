import json 

from infrastructure.log_wrapper import LogWrapper
from models.trade_settings import TradeSettings

class Bot:

    ERROR_LOG = "error"
    MAIN_LOG = "main"

    def __init__(self):
        self.load_settings()
        self.setup_logs()
        self.log_to_main("Bot started")
        self.log_to_error("Bot started")

    def load_settings(self):
        with open('./bot/settings.json', 'r') as f:
            data = json.loads(f.read())
            # Keys are "GBP_CHF" and "EUR_CHF", values are dictionaries
            self.trade_settings = { k: TradeSettings(v, k) for k, v in data.items()}

    def setup_logs(self):
        self.logs = {}
        for k in self.trade_settings.keys():
            self.logs[k] = LogWrapper(k)
            self.log_message(f"{self.trade_settings[k]}", k)
        self.logs[Bot.ERROR_LOG] = LogWrapper(Bot.ERROR_LOG)
        self.logs[Bot.MAIN_LOG] = LogWrapper(Bot.MAIN_LOG)
        self.log_to_main(f"Bot started with {TradeSettings.settings_to_str(self.trade_settings)}")

    def log_message(self, msg, key):
        # .debug actually logs the messages
        self.logs[key].logger.debug(msg)

    def log_to_main(self, msg):
        self.log_message(msg, Bot.MAIN_LOG)

    def log_to_error(self, msg):
        self.log_message(msg, Bot.ERROR_LOG)

