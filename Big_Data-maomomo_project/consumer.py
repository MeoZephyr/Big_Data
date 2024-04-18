import json
from pymongo import MongoClient

with open("config.json", "r") as f:
    config:dict = json.load(f)

client = MongoClient(cofig["connect_str"])
db = client[config["db_name"]]
db["RealTimeNearStop"].delete_many({})
db["StopOfRoute"].delete_many({})

with open("./data/route.json", "r") as g:
    sor = json.load(g)

with open("./data/route.json", "r") as g:
    sor = json.load(g)

data = {}

for i in 




for i, j in data.items():
    insert_data = {"_id":i, "data":j}
    db["RealTimeNearStop"].insert_one(insert_data)
db["StopOfRoute"].insert_many(sor)