from flask import Flask, request, make_response, jsonify
from service.usuarioService import findAllUsuarios, findUser, verifyUser
from service.atividadesService import findUserAtividade, ordenaPrioridade, ordenaData, insertAtividade, updateAtividade, findAtividade, deleteAtividade
from flask_cors import CORS
import json

server = Flask(__name__)
server.json.sort_keys = False
CORS(server)

@server.route('/users', methods=['GET'])
def users():
    return jsonify(findAllUsuarios()), 200

@server.route('/login', methods=['POST'])
def login():
    user = request.json
    id_usuario, nome_usuario, status_code = findUser(user)

    if(status_code == 200):
        return jsonify({"id_usuario": id_usuario, "nome_usuario": nome_usuario}), status_code
    return jsonify({"message": "Informações de login inválidas"}), status_code

@server.route('/cadastro', methods=['POST'])
def cadastro():
    user = request.json
    return verifyUser(user)

# 
# ATIVIDADES
# 
    # CRUD
    ################

@server.route('/<user_id>/atividades', methods=['GET'])
def user_atividades(user_id):
    return jsonify(findUserAtividade(user_id)), 200

@server.route('/atividade/<atv_id>', methods=['GET'])
def get_atividade(atv_id):
    return findAtividade(str(atv_id))

@server.route('/<user_id>/atividades/nova', methods=['POST'])
def nova_atividade(user_id):
    atividade = request.json
    return insertAtividade(atividade, user_id)

@server.route('/atividade/<atv_id>/update', methods=['POST'])
def update_atividade(atv_id):
    atividade = request.json
    return updateAtividade(atividade, atv_id)

@server.route('/atividade/<atv_id>', methods=['DELETE'])
def delete_atividade(atv_id):
    return deleteAtividade(atv_id)

    # ORDENAÇÕES
    ################

@server.route('/<user_id>/atividades/prioridade', methods=['GET'])
def atividades_prioridade(user_id):
    return jsonify(ordenaPrioridade(user_id)), 200

@server.route('/<user_id>/atividades/data', methods=['GET'])
def atividades_data(user_id):
    return jsonify(ordenaData(user_id)), 200

    
server.run()