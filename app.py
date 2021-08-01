from flask import Flask, render_template
from bson.json_util import dumps
import pymongo

def page_not_found(e):
    return render_template('index.html'), 404

app = Flask(__name__)

app.register_error_handler(404, page_not_found)

conn = pymongo.MongoClient("localhost", 27017)
db = conn.thoth_db
col = db.postit

@app.route('/all', methods=['GET'])
def get():
    data = list(col.find())
    return dumps(data, ensure_ascii=False)