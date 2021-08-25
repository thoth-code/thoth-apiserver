from bson.json_util import dumps
import models

def sign_in(user):
    data = models.signin(user)
    if data:
        return data
    else:
        return dumps({"error":"UserNotFoundException"})

def sign_up(user):
    if not models.emailAlreadyExists(user['email']):
        models.signup(user)
        return dumps({"error":None})
    else:
        return dumps({"error":"EmailAlreadyExistsException"})

def get_notes(param):
    data = models.getNotes(param)
    return dumps(data, ensure_ascii=False)

def post_note(note):
    if models.verify():
        models.postNote(note)
        return dumps({"error":None})
    else:
        return dumps({"error":"VerificationException"})

def update_note(note):
    if models.verify():
        if models.noteExists(note['nid']):
            models.updateNote(note)
            return dumps({"error":None})
        else:
            return dumps({"error":"NoteNotFoundException"})
    else:
        return dumps({"error":"VerificationException"})

def delete_note(nid):
    if models.verify():
        if models.noteExists(nid):
            models.deleteNote(nid)
            return dumps({"error":None})
        else:
            return dumps({"error":"NoteNotFoundException"})
    else:
        return dumps({"error":"VerificationException"})

def get_mynote():
    if models.verify():
        data = models.getMynote()
        return dumps(data, ensure_ascii=False)
    else:
        return dumps({"error":"VerificationException"})

def post_mynote(nid):
    if models.verify():
        if models.noteExists(nid):
            if not models.scrabAlreadyExists(nid):
                models.postMynote(nid)
                return dumps({"error":None})
            else:
                return dumps({"error":"ScrabAlreadyExistsException"})
        else:
            return dumps({"error":"NoteNotFoundException"})
    else:
        return dumps({"error":"VerificationException"})

def delete_mynote(nid):
    if models.verify():
        if models.scrabExists(nid):
            models.deleteMynote(nid)
            return dumps({"error":None})
        else:
            return dumps({"error":"ScrabNotFoundException"})
    else:
        return dumps({"error":"VerificationException"})
