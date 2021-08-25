from flask import make_response, request
from bson.objectid import ObjectId
import pymongo, jwt, hashlib

conn = pymongo.MongoClient("localhost", 27017)
db = conn.thoth_db

def verify():
    col = db.user
    encoded = request.cookies.get('accessToken')
    decoded = jwt.decode(encoded, 'JEfWefI0E1qlnIz06qmob7cZp5IzH/i7KwOI2xqWfhE=', algorithms=["HS256"])
    result = col.find_one({'_id': ObjectId(decoded['uid'])})
    return result

def get_uid():
    col = db.user
    encoded = request.cookies.get('accessToken')
    decoded = jwt.decode(encoded, 'JEfWefI0E1qlnIz06qmob7cZp5IzH/i7KwOI2xqWfhE=', algorithms=["HS256"])
    return decoded['uid']

def note_exists(nid):
    col = db.note
    data = col.find_one({"_id": ObjectId(nid)})
    return data

def scrab_exists(nid):
    col = db.scrab
    data = col.find_one({"_id": ObjectId(nid)})
    return data

def scrab_already_exists(nid):
    col = db.note
    result = col.find_one({"_id": ObjectId(nid)})
    col = db.scrab
    data = col.find_one({"uid":getUid(), "onid":str(result['_id'])})
    return data

def email_already_exists(email):
    col = db.user
    data = col.find_one({"email": email})
    return data

def sign_in(user):
    col = db.user
    m = hashlib.sha256()
    pwd = user['password']
    m.update(pwd.encode('utf-8'))
    user['password'] = m.hexdigest()
    result = col.find_one(user)
    if result:
        encoded = jwt.encode({"uid":str(result['_id'])}, 'JEfWefI0E1qlnIz06qmob7cZp5IzH/i7KwOI2xqWfhE=', algorithm='HS256')
        resp = make_response('{"error": null}')
        resp.set_cookie('accessToken', encoded, max_age=60*60*2)
        return resp
    else:
        return None

def sign_up(user):
    col = db.user
    m = hashlib.sha256()
    pwd = user['password']
    m.update(pwd.encode('utf-8'))
    user['password'] = m.hexdigest()
    col.insert_one(user)

def get_notes(param):
    col = db.note
    count = int(param.get('count'))*10
    data = list(col.find().skip(count).limit(10))
    return data

def post_note(note):
    col = db.note
    note['uid'] = getUid()
    col.insert_one(note)

def update_note(note):
    col = db.note
    nid = note['nid']
    result = col.update_one({"_id": ObjectId(nid)}, {"$set":note})

def delete_note(nid):
    col = db.note
    col.delete_one({"_id": ObjectId(nid)})

def get_mynote():
    col = db.scrab
    uid = getUid()
    data = list(col.find({"uid": uid}))
    return data

def post_mynote(nid):
    col = db.note
    result = col.find_one({"_id": ObjectId(nid)})
    data = {}
    data['title'] = result['title']
    data['code'] = result['code']
    data['tag'] = result['tag']
    data['ref'] = result['ref']
    data['uid'] = getUid()
    data['onid'] = str(result['_id'])
    col = db.scrab
    col.insert(data)

def delete_mynote(nid):
    col = db.scrab
    col.delete_one({"_id": ObjectId(nid)})
