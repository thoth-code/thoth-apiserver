from flask import Blueprint, request, make_response
from bson.json_util import dumps
import pymongo, jwt

bp = Blueprint('main', __name__, url_prefix='/api')

conn = pymongo.MongoClient("localhost", 27017)
db = conn.thoth_db

@bp.route('/notes', methods=['GET'])
def get():
    col = db.postit
    data = list(col.find())
    return dumps(data, ensure_ascii=False)

@bp.route('/notes', methods=['POST'])
def post():
    col = db.postit
    postit = {}
    postit['title'] = request.form['title']
    postit['code'] = request.form['code']
    postit['tag'] = request.form['tag']
    col.insert_one(postit)
    return '{"error":null}'

@bp.route('/signin', methods=['POST'])
def login():
    col = db.user
    user = {}
    user['email'] = request.form['email']
    user['password'] = request.form['password']
    result = col.find_one(user)
    if result:
        data = {}
        data['email'] = user['email']
        encoded = jwt.encode(data, 'JEfWefI0E1qlnIz06qmob7cZp5IzH/i7KwOI2xqWfhE=', algorithm='HS256')
        resp = make_response("Login successful.")
        resp.set_cookie('accessToken', encoded)
        return resp
    else:
        return 'User not found.'