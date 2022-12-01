from pymongo import MongoClient

from utils.config import config


def init_DB(db_name: str):
    connection: MongoClient = MongoClient(config.db.host, config.db.port)
    db = connection[db_name]
    return db


db = init_DB(config.db.main_database)


def get_collection(collection_name: str):
    return db[collection_name]


run_log_db = db.system_log
monitor_log_db = db.monitor_log
