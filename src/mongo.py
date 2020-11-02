from pymongo import MongoClient

def connect_mongo():
    global client
    client = MongoClient('localhost', 27017)

def connect_coll(db_name, coll_name):
    global coll
    db = client[db_name]
    coll = db[coll_name]

def insert_one(d):
    coll.insert(d)

def close_mongo():
    client.close()