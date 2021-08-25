from flask import Blueprint, request
import service

bp = Blueprint('main', __name__, url_prefix='/api')

@bp.route('/signin', methods=['POST'])
def sign_in():
    user = request.get_json()
    data = service.signin(user)
    return data

@bp.route('/signup', methods=['POST'])
def sign_up():
    user = request.get_json()
    data = service.signup(user)
    return data

@bp.route('/notes', methods=['GET'])
def get_notes():
    param = request.args
    data = service.getNotes(param)
    return data

@bp.route('/note', methods=['POST'])
def post_note():
    note = request.get_json()
    data = service.postNote(note)
    return data

@bp.route('/note', methods=['PUT'])
def update_note():
    note = request.get_json()
    data = service.updateNote(note)
    return data

@bp.route('/note/<nid>', methods=['DELETE'])
def delete_note(nid):
    data = service.deleteNote(nid)
    return data

@bp.route('/myboard', methods=['GET'])
def get_mynote():
    data = service.getMynote()
    return data

@bp.route('/myboard', methods=['POST'])
def post_mynote():
    temp = request.get_json()
    nid = temp['nid']
    data = service.postMynote(nid)
    return data

@bp.route('/myboard/<nid>', methods=['DELETE'])
def delete_mynote(nid):
    data = service.deleteMynote(nid)
    return data
