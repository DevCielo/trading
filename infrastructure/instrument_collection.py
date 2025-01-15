import json
from models.instrument import Instrument
from db.db import DataDB


class InstrumentCollection:
    FILENAME = "instruments.json"
    API_KEYS = ["name", "type", "displayName", "pipLocation", "displayPrecision", "tradeUnitsPrecision", "marginRate"]

    def __init__(self):
        self.instruments_dict = {}

    def LoadInstruments(self, path):
        self.instruments_dict = {}
        fileName = f"{path}/{self.FILENAME}"
        with open(fileName, "r") as f:
            data = json.loads(f.read())

            for k, v in data.items():
                # KEY is the name of the instrument, value is the whole dictionary
                self.instruments_dict[k] = Instrument.FromApiObject(v)

    def LoadInstrumentsDB(self):
        self.instruments_dict = {}
        data = DataDB().query_single(DataDB.INSTRUMENTS_COLL)
        for k, v in data.items():
            self.instruments_dict[k] = Instrument.FromApiObject(v)

    def CreateFile(self, data, path):
        if data is None:
            print("Instrument file creation failed")
            return

        instruments_dict = {}
        for i in data:
            key = i['name']
            instruments_dict[key] = { k: i[k] for k in self.API_KEYS }

        fileName = f"{path}/{self.FILENAME}"
        with open(fileName, "w") as f:
            f.write(json.dumps(instruments_dict, indent=2))

    def CreateDB(self, data):
        if data is None:
            print("Instrument file creation failed")
            return

        instruments_dict = {}
        for i in data:
            key = i['name']
            instruments_dict[key] = { k: i[k] for k in self.API_KEYS }
        
        database = DataDB()
        database.delete_many(DataDB.INSTRUMENTS_COLL)
        database.add_one(DataDB.INSTRUMENTS_COLL, instruments_dict)

    def PrintInstruments(self):
        [print(k, v) for k,v in self.instruments_dict.items()]
        print(len(self.instruments_dict.keys()), "instruments")

instrumentCollection = InstrumentCollection()