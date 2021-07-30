import pymongo
from bson.json_util import dumps
conn = pymongo.MongoClient("localhost", 27017)
db = conn.thoth_db
col = db.postit
data = (list(col.find()))
print(data[0])