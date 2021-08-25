from flask import Blueprint, request
import service

bp = Blueprint('main', __name__, url_prefix='/api')

@bp.route('/signin', methods=['POST'])
def sign_in():
    user = request.get_json()
    data = service.sign_in(user)
    return data

@bp.route('/signup', methods=['POST'])
def sign_up():
    user = request.get_json()
    data = service.sign_up(user)
    return data

@bp.route('/notes', methods=['GET'])
def get_notes():
    param = request.args
    data = service.get_notes(param)
    return data

@bp.route('/note', methods=['POST'])
def post_note():
    note = request.get_json()
    data = service.post_note(note)
    return data

@bp.route('/note', methods=['PUT'])
def update_note():
    note = request.get_json()
    data = service.update_note(note)
    return data

@bp.route('/note/<nid>', methods=['DELETE'])
def delete_note(nid):
    data = service.delete_note(nid)
    return data

@bp.route('/myboard', methods=['GET'])
def get_mynote():
    data = service.get_mynote()
    return data

@bp.route('/myboard', methods=['POST'])
def post_mynote():
    temp = request.get_json()
    nid = temp['nid']
    data = service.post_mynote(nid)
    return data

@bp.route('/myboard/<nid>', methods=['DELETE'])
def delete_mynote(nid):
    data = service.delete_mynote(nid)
    return data
