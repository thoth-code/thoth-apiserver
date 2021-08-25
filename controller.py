from flask import Blueprint, request
import service

bp = Blueprint('main', __name__, url_prefix='/api')

@bp.route('/signin', methods=['POST'])
def signin():
    user = request.get_json()
    data = service.signin(user)
    return data

@bp.route('/signup', methods=['POST'])
def signup():
    user = request.get_json()
    data = service.signup(user)
    return data

@bp.route('/notes', methods=['GET'])
def getNotes():
    data = service.getNotes()
    return data

@bp.route('/note', methods=['POST'])
def postNote():
    note = request.get_json()
    data = service.postNote(note)
    return data

@bp.route('/note', methods=['PUT'])
def updateNote():
    note = request.get_json()
    data = service.updateNote(note)
    return data

@bp.route('/note/<nid>', methods=['DELETE'])
def deleteNote(nid):
    data = service.deleteNote(nid)
    return data

@bp.route('/myboard', methods=['GET'])
def getMynote():
    data = service.getMynote()
    return data

@bp.route('/myboard', methods=['POST'])
def postMynote():
    temp = request.get_json()
    nid = temp['nid']
    data = service.postMynote(nid)
    return data

@bp.route('/myboard/<nid>', methods=['DELETE'])
def deleteMynote(nid):
    data = service.deleteMynote(nid)
    return data
