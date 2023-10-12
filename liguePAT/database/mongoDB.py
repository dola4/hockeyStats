from pymongo import MongoClient


def connection():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['ligue_pat']
    return db
