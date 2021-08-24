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

def getUid():
    col = db.user
    encoded = request.cookies.get('accessToken')
    decoded = jwt.decode(encoded, 'JEfWefI0E1qlnIz06qmob7cZp5IzH/i7KwOI2xqWfhE=', algorithms=["HS256"])
    return decoded['uid']

def noteExists(nid):
    col = db.note
    data = col.find_one({"_id": ObjectId(nid)})
    return data

def scrabAlreadyExists(nid):
    col = db.scrab
    data = col.find_one({"_id": ObjectId(nid)})
    return data

def emailAlreadyExists(email):
    col = db.user
    data = col.find_one({"email": email})
    return data

def signin(user):
    col = db.user
    m = hashlib.sha256()
    pwd = user['password']
    m.update(pwd.encode('utf-8'))
    user['password'] = m.hexdigest()
    result = col.find_one(user)
    if result:
        encoded = jwt.encode({"uid":str(result['_id'])}, 'JEfWefI0E1qlnIz06qmob7cZp5IzH/i7KwOI2xqWfhE=', algorithm='HS256')
        resp = make_response('{"error": null}')
        resp.set_cookie('accessToken', encoded)
        return resp
    else:
        return None

def signup(user):
    col = db.user
    m = hashlib.sha256()
    pwd = user['password']
    m.update(pwd.encode('utf-8'))
    user['password'] = m.hexdigest()
    col.insert_one(user)

def getNotes():
    col = db.note
    data = list(col.find())
    return data

def postNote(note):
    col = db.note
    note['uid'] = getUid()
    col.insert_one(note)

def updateNote(note):
    col = db.note
    nid = note['nid']
    result = col.update_one({"_id": ObjectId(nid)}, {"$set":note})

def deleteNote(nid):
    col = db.note
    col.delete_one({"_id": ObjectId(nid)})

def getMynote():
    col = db.scrab
    uid = getUid()
    data = list(col.find({"uid": uid}))
    return data

def postMynote(nid):
    col = db.note
    result = col.find_one({'_id': ObjectId(nid)})
    col = db.scrab
    col.insert(result)

def deleteMynote(nid): 
    col = db.scrab
    col.delete_one({'_id': ObjectId(nid)})
