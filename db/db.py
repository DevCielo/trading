from pymongo import MongoClient, errors

import os
from dotenv import load_dotenv

load_dotenv(verbose=False)

MONGO_CONN_STR = os.getenv("MONGO_CONN_STR")

class DataDB:
    SAMPLE_COLL = "forex"
    CALENDAR_COLL = "forex_calendar"
    INSTRUMENTS_COLL = "forex_instruments"

    def __init__(self):
        self.client = MongoClient(MONGO_CONN_STR)
        self.db = self.client.forex

    def test_connection(self):
        print(self.db.list_collection_names())

    def delete_many(self, collection, **kwargs):
        try:
            _ = self.db[collection].delete_many(kwargs)

        except errors.InvalidOperation:
            print("delete_many error:", error)

    def add_one(self, collection, ob):
        try:
            _ = self.db[collection].insert_one(ob)

        except errors.InvalidOperation:
            print("add_one error:", error)

    def add_many(self, collection, list_ob):
        try:
            self.db[collection].insert_many(list_ob)

        except errors.InvalidOperation:
            print("add_many error:", error)

    def query_distinct(self, collection, **kwargs):
        try:
            r = self.db[collection].distinct(key)
            return r

        except errors.InvalidOperation:
            print("query_distinct error:", error)

    def query_single(self, collection, **kwargs):
        try:
            r = self.db[collection].find_one(kwargs, {'_id': 0})
            return r

        except errors.InvalidOperation:
            print("query_single error:", error)


    def query_all(self, collection, **kwargs):
        try:
            data = []
            r = self.db[collection].find(kwargs, {'_id': 0})
            for item in r:
                data.append(item)
            return data

        except errors.InvalidOperation:
            print("query_all error:", error)