from flask import Blueprint, request, make_response
from bson.json_util import dumps
from bson.objectid import ObjectId
import pymongo, jwt, hashlib

bp = Blueprint('main', __name__, url_prefix='/api')

conn = pymongo.MongoClient("localhost", 27017)
db = conn.thoth_db

@bp.route('/notes', methods=['GET'])
def get():
    col = db.note
    data = list(col.find())
    return dumps(data, ensure_ascii=False)

@bp.route('/notes', methods=['POST'])
def post():
    col = db.note
    note = {}
    note['uid'] = request.form['uid']
    note['title'] = request.form['title']
    note['code'] = request.form['code']
    note['tag'] = request.form['tag']
    note['ref'] = request.form['ref']
    col.insert_one(note)
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
        encoded = jwt.encode({'uid':str(result['_id'])}, 'JEfWefI0E1qlnIz06qmob7cZp5IzH/i7KwOI2xqWfhE=', algorithm='HS256')
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
    col = db.note
    note = {}
    nid = request.form['nid']
    note['title'] = request.form['title']
    note['code'] = request.form['code']
    note['tag'] = request.form['tag']
    note['ref'] = request.form['ref']
    result = col.update_one({'_id': ObjectId(nid)}, {"$set":note})
    return dumps({'error':None})

@bp.route('/note/<nid>', methods=['DELETE'])
def delete(nid):
    col = db.note
    col.delete_one({'_id': ObjectId(nid)})
    return dumps({'error':None})

@bp.route('/myboard', methods=['POST'])
def scrab():
    col = db.note
    nid = request.form['nid']
    result = col.find_one({'_id': ObjectId(nid)})
    col = db.scrab
    col.insert(result)
    return dumps({'error':None})