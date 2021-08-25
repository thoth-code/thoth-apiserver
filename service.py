from bson.json_util import dumps
import models

def signin(user):
    data = models.signin(user)
    if data:
        return data
    else:
        return dumps({"error":"userNotFoundException"})

def signup(user):
    if not models.emailAlreadyExists(user['email']):
        models.signup(user)
        return dumps({"error":None})
    else:
        return dumps({"error":"emailAlreadyExistsException"})

def getNotes():
    data = models.getNotes()
    return dumps(data, ensure_ascii=False)

def postNote(note):
    if models.verify():
        models.postNote(note)
        return dumps({"error":None})
    else:
        return dumps({"error":"loginFailedException"})

def updateNote(note):
    if models.verify():
        if models.noteExists(note['nid']):
            models.updateNote(note)
            return dumps({"error":None})
        else:
            return dumps({"error":"noteNotFoundException"})
    else:
        return dumps({"error":"loginFailedException"})

def deleteNote(nid):
    if models.verify():
        if models.noteExists(nid):
            models.deleteNote(nid)
            return dumps({"error":None})
        else:
            return dumps({"error":"noteNotFoundException"})
    else:
        return dumps({"error":"loginFailedException"})

def getMynote():
    if models.verify():
        data = models.getMynote()
        return dumps(data, ensure_ascii=False)
    else:
        return dumps({"error":"loginFailedException"})

def postMynote(nid):
    if models.verify():
        if models.noteExists(nid):
            if not models.scrabAlreadyExists(nid):
                models.postMynote(nid)
                return dumps({"error":None})
            else:
                return dumps({"error":"scrabAlreadyExistsException"})
        else:
            return dumps({"error":"noteNotFoundException"})
    else:
        return dumps({"error":"loginFailedException"})

def deleteMynote(nid):
    if models.verify():
        if models.noteExists(nid):
            return dumps({"error":None})
        else:
            return dumps({"error":"noteNotFoundException"})
    else:
        return dumps({"error":"loginFailedException"})
