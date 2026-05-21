from flask import Blueprint, request, jsonify
from service.usuario_service import UsuarioService
from service.autenticacao_service import AutenticacaoService
from model.usuario import (
    EmailJaCadastrado,
    UsuarioNaoEncontrado,
    SenhaInvalida,
    EmailInvalido,
    SenhaMuitoCurta,
    NomeInvalido,
)

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
    except EmailInvalido:
        return jsonify({"erro": "Email invalido"}), 400
    except SenhaMuitoCurta:
        return jsonify({"erro": "Senha precisa ter pelo menos 6 caracteres"}), 400
    except NomeInvalido:
        return jsonify({"erro": "Nome invalido"}), 400


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


@usuario_bp.route('/auth/me', methods=['GET'])
def buscar_me():
    usuario = AutenticacaoService.instancia().obter_usuario_autenticado()
    if not usuario:
        return jsonify({"erro": "Token invalido ou ausente"}), 401
    return jsonify({
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "token_api": usuario.token_api
    })


@usuario_bp.route('/auth/me', methods=['PUT'])
def atualizar_me():
    usuario = AutenticacaoService.instancia().obter_usuario_autenticado()
    if not usuario:
        return jsonify({"erro": "Token invalido ou ausente"}), 401

    dados = request.get_json()
    try:
        usuario = UsuarioService.instancia().atualizar(
            usuario,
            nome=dados.get('nome'),
            email=dados.get('email'),
            senha=dados.get('senha')
        )
        return jsonify({
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "token_api": usuario.token_api
        })
    except EmailJaCadastrado:
        return jsonify({"erro": "Email ja cadastrado"}), 409
    except EmailInvalido:
        return jsonify({"erro": "Email invalido"}), 400
    except SenhaMuitoCurta:
        return jsonify({"erro": "Senha precisa ter pelo menos 6 caracteres"}), 400
    except NomeInvalido:
        return jsonify({"erro": "Nome invalido"}), 400
