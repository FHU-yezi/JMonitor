from pymongo import MongoClient

from config_manager import config


def InitDB():
    connection: MongoClient = MongoClient(config["db_address"],
                                          config["db_port"])
    db = connection.JMonitorData
    return db


db = InitDB()

run_log_db = db.system_log
monitor_log_db = db.monitor_log
