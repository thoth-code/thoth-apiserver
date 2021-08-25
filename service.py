from bson.json_util import dumps
import models

def sign_in(user):
    data = models.sign_in(user)
    if data:
        return data
    else:
        return dumps({"error":"UserNotFoundException"})

def sign_up(user):
    if not models.email_already_exists(user['email']):
        models.sign_up(user)
        return dumps({"error":None})
    else:
        return dumps({"error":"EmailAlreadyExistsException"})

def get_notes(param):
    data = models.get_notes(param)
    return dumps(data, ensure_ascii=False)

def post_note(note):
    if models.verify():
        models.post_note(note)
        return dumps({"error":None})
    else:
        return dumps({"error":"VerificationException"})

def update_note(note):
    if models.verify():
        if models.note_exists(note['nid']):
            models.update_note(note)
            return dumps({"error":None})
        else:
            return dumps({"error":"NoteNotFoundException"})
    else:
        return dumps({"error":"VerificationException"})

def delete_note(nid):
    if models.verify():
        if models.note_exists(nid):
            models.delete_note(nid)
            return dumps({"error":None})
        else:
            return dumps({"error":"NoteNotFoundException"})
    else:
        return dumps({"error":"VerificationException"})

def get_mynote():
    if models.verify():
        data = models.get_mynote()
        return dumps(data, ensure_ascii=False)
    else:
        return dumps({"error":"VerificationException"})

def post_mynote(nid):
    if models.verify():
        if models.note_exists(nid):
            if not models.scrab_already_exists(nid):
                models.post_mynote(nid)
                return dumps({"error":None})
            else:
                return dumps({"error":"ScrabAlreadyExistsException"})
        else:
            return dumps({"error":"NoteNotFoundException"})
    else:
        return dumps({"error":"VerificationException"})

def delete_mynote(nid):
    if models.verify():
        if models.scrab_exists(nid):
            models.delete_mynote(nid)
            return dumps({"error":None})
        else:
            return dumps({"error":"ScrabNotFoundException"})
    else:
        return dumps({"error":"VerificationException"})
