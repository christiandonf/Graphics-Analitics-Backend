from flask import Blueprint, request, jsonify
from service.usuario_service import UsuarioService
from model.usuario import EmailJaCadastrado, UsuarioNaoEncontrado, SenhaInvalida

usuario_bp = Blueprint('usuario', __name__)


@usuario_bp.route('/auth/registro', methods=['POST'])
def registrar():
    dados = request.get_json()
    try:
        usuario = UsuarioService.instancia().registrar(
            nome=dados['nome'],
            email=dados['email'],
            senha=dados['senha']
        )
        return jsonify({
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "token_api": usuario.token_api
        }), 201
    except EmailJaCadastrado:
        return jsonify({"erro": "Email ja cadastrado"}), 409


@usuario_bp.route('/auth/login', methods=['POST'])
def login():
    dados = request.get_json()
    try:
        usuario = UsuarioService.instancia().login(
            email=dados['email'],
            senha=dados['senha']
        )
        return jsonify({
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "token_api": usuario.token_api
        })
    except UsuarioNaoEncontrado:
        return jsonify({"erro": "Email nao encontrado"}), 404
    except SenhaInvalida:
        return jsonify({"erro": "Senha invalida"}), 401


@usuario_bp.route('/auth/usuario/<int:id>', methods=['GET'])
def buscar(id):
    try:
        usuario = UsuarioService.instancia().buscar_por_id(id)
        return jsonify({
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "token_api": usuario.token_api
        })
    except UsuarioNaoEncontrado:
        return jsonify({"erro": "Usuario nao encontrado"}), 404
