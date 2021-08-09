from flask import Blueprint, request
from bson.json_util import dumps
import pymongo

bp = Blueprint('main', __name__, url_prefix='/api')

conn = pymongo.MongoClient("localhost", 27017)
db = conn.thoth_db
col = db.postit

@bp.route('/notes', methods=['GET'])
def get():
    data = list(col.find())
    return dumps(data, ensure_ascii=False)

@bp.route('/notes', methods=['POST'])
def post():
    postit = {}
    postit['title'] = request.form['title']
    postit['code'] = request.form['code']
    postit['tag'] = request.form['tag']
    col.insert_one(postit)
    return '{"error":null}'

