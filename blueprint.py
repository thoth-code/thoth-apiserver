from flask import Blueprint
from bson.json_util import dumps
import pymongo

bp = Blueprint('main', __name__, url_prefix='/')

conn = pymongo.MongoClient("localhost", 27017)
db = conn.thoth_db
col = db.postit

@bp.route('/all', methods=['GET'])
def get():
    data = list(col.find())
    return dumps(data, ensure_ascii=False)