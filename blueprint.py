from flask import Blueprint, request, make_response
from bson.json_util import dumps
from bson.objectid import ObjectId
import pymongo, jwt, hashlib

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
    postit['uid'] = request.form['uid']
    postit['title'] = request.form['title']
    postit['code'] = request.form['code']
    postit['tag'] = request.form['tag']
    postit['ref'] = request.form['ref']
    col.insert_one(postit)
    return dumps({'error':None})

@bp.route('/signin', methods=['POST'])
def signin():
    col = db.user
    m = hashlib.sha256()
    user = {}
    user['email'] = request.form['email']
    pwd = request.form['password']
    m.update(pwd.encode('utf-8'))
    user['password'] = m.hexdigest()
    result = col.find_one(user)
    if result:
        data = {}
        data['email'] = user['email']
        encoded = jwt.encode(data, 'JEfWefI0E1qlnIz06qmob7cZp5IzH/i7KwOI2xqWfhE=', algorithm='HS256')
        resp = make_response('{"error":null}')
        resp.set_cookie('accessToken', encoded)
        return resp
    else:
        return dumps({'error':'UserNotFound'})

@bp.route('/signup', methods=['POST'])
def signup():
    col = db.user
    m = hashlib.sha256()
    user = {}
    user['email'] = request.form['email']
    pwd = request.form['password']
    m.update(pwd.encode('utf-8'))
    user['password'] = m.hexdigest()
    col.insert_one(user)
    return dumps({'error':None})

@bp.route('/note', methods=['PUT'])
def update():
    col = db.postit
    postit = {}
    nid = request.form['nid']
    postit['title'] = request.form['title']
    postit['code'] = request.form['code']
    postit['tag'] = request.form['tag']
    postit['ref'] = request.form['ref']
    result = col.update_one({'_id': ObjectId(nid)}, {"$set":postit})
    return jsonify({"error":null})

@bp.route('/note/<nid>', methods=['DELETE'])
def delete(nid):
    col = db.postit
    col.delete_one({'_id': ObjectId(nid)})
    return dumps({'error':None})
