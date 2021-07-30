from flask import Flask
from bson.json_util import dumps
import pymongo

app = Flask(__name__)

conn = pymongo.MongoClient("localhost", 27017)
db = conn.thoth_db
col = db.postit

@app.route('/all', methods=['GET'])
def get():
    data = list(col.find())
    return dumps(data, ensure_ascii=False)