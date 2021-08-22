from flask import Blueprint, request, make_response
from bson.json_util import dumps
from bson.objectid import ObjectId
import pymongo, jwt, hashlib

bp = Blueprint('main', __name__, url_prefix='/api')

conn = pymongo.MongoClient("localhost", 27017)
db = conn.thoth_db

def verify(db):
    col = db.user
    encoded = request.cookies.get('accessToken')
    decoded = jwt.decode(encoded, 'JEfWefI0E1qlnIz06qmob7cZp5IzH/i7KwOI2xqWfhE=', algorithms=["HS256"])
    result = col.find_one({'_id': ObjectId(decoded['uid'])})
    return result

@bp.route('/notes', methods=['GET'])
def get():
    col = db.note
    data = list(col.find())
    return dumps(data, ensure_ascii=False)

@bp.route('/note', methods=['POST'])
def post():
    col = db.user
    encoded = request.cookies.get('accessToken')
    decoded = jwt.decode(encoded, 'JEfWefI0E1qlnIz06qmob7cZp5IzH/i7KwOI2xqWfhE=', algorithms=["HS256"])
    result = col.find_one({'_id': ObjectId(decoded['uid'])})
    if result:
        col = db.note
        note = request.get_json()
        note['uid'] = decoded['uid']
        col.insert_one(note)
        return dumps({'error':None})
    else:
        return dumps({'error':'LoginNotVerified'})

@bp.route('/signin', methods=['POST'])
def signin():
    col = db.user
    m = hashlib.sha256()
    user = request.get_json()
    pwd = user['password']
    m.update(pwd.encode('utf-8'))
    user['password'] = m.hexdigest()
    result = col.find_one(user)
    if result:
        encoded = jwt.encode({'uid':str(result['_id'])}, 'JEfWefI0E1qlnIz06qmob7cZp5IzH/i7KwOI2xqWfhE=', algorithm='HS256')
        resp = make_response('{"error": null}')
        resp.set_cookie('accessToken', encoded)
        return resp
    else:
        return dumps({'error':'UserNotFound'})

@bp.route('/signup', methods=['POST'])
def signup():
    col = db.user
    m = hashlib.sha256()
    user = request.get_json()
    pwd = user['password']
    m.update(pwd.encode('utf-8'))
    user['password'] = m.hexdigest()
    col.insert_one(user)
    return dumps({'error':None})

@bp.route('/note', methods=['PUT'])
def update():
    if verify(db):
        col = db.note
        note = request.get_json()
        nid = note['nid']
        result = col.update_one({'_id': ObjectId(nid)}, {"$set":note})
        return dumps({'error':None})
    else:
        return dumps({'error':'LoginNotVerified'})

@bp.route('/note/<nid>', methods=['DELETE'])
def delete(nid):
    if verify(db):
        col = db.note
        col.delete_one({'_id': ObjectId(nid)})
        return dumps({'error':None})
    else:
        return dumps({'error':'LoginNotVerified'})

@bp.route('/myboard', methods=['POST'])
def scrab():
    if verify(db):
        col = db.note
        data = request.get_json()
        nid = data['nid']
        result = col.find_one({'_id': ObjectId(nid)})
        col = db.scrab
        col.insert(result)
        return dumps({'error':None})
    else:
        return dumps({'error':'LoginNotVerified'})

@bp.route('/myboard/<nid>', methods=['DELETE'])
def unscrab(nid):
    if verify(db):
        col = db.scrab
        col.delete_one({'_id': ObjectId(nid)})
        return dumps({'error':None})
    else:
        return dumps({'error':'LoginNotVerified'})

@bp.route('/myboard', methods=['GET'])
def getcrab():
    col = db.scrab
    data = list(col.find())
    return dumps(data, ensure_ascii=False)