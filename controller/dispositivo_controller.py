from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from service.dispositivo_service import DispositivoService
from service.autenticacao_service import AutenticacaoService
from model.dispositivo import DispositivoNaoEncontrado

dispositivo_bp = Blueprint('dispositivo', __name__)


@dispositivo_bp.route('/dispositivos', methods=['POST'])
@cross_origin(origin='*')
def criar():
    usuario = AutenticacaoService.instancia().obter_usuario_autenticado()
    if not usuario:
        return jsonify({"erro": "Token invalido ou ausente"}), 401

    dados = request.get_json()
    dispositivo = DispositivoService.instancia().criar(
        usuario_id=usuario.id,
        nome=dados['nome'],
        descricao=dados.get('descricao')
    )
    return jsonify({
        "id": dispositivo.id,
        "usuario_id": dispositivo.usuario_id,
        "nome": dispositivo.nome,
        "descricao": dispositivo.descricao,
        "chave": dispositivo.chave,
        "ativo": dispositivo.ativo
    }), 201


@dispositivo_bp.route('/dispositivos', methods=['GET'])
def listar():
    usuario = AutenticacaoService.instancia().obter_usuario_autenticado()
    if not usuario:
        return jsonify({"erro": "Token invalido ou ausente"}), 401

    dispositivos = DispositivoService.instancia().listar_por_usuario(usuario.id)
    return jsonify([{
        "id": d.id,
        "nome": d.nome,
        "descricao": d.descricao,
        "chave": d.chave,
        "ativo": d.ativo
    } for d in dispositivos])


@dispositivo_bp.route('/dispositivos/<chave>', methods=['PUT'])
@cross_origin(origin='*')
def atualizar(chave):
    usuario = AutenticacaoService.instancia().obter_usuario_autenticado()
    if not usuario:
        return jsonify({"erro": "Token invalido ou ausente"}), 401

    try:
        dispositivo = DispositivoService.instancia().buscar_por_chave(chave)
        if dispositivo.usuario_id != usuario.id:
            return jsonify({"erro": "Dispositivo nao pertence a este usuario"}), 403

        dados = request.get_json()
        dispositivo = DispositivoService.instancia().atualizar(
            dispositivo,
            nome=dados.get('nome'),
            descricao=dados.get('descricao'),
            ativo=dados.get('ativo')
        )
        return jsonify({
            "id": dispositivo.id,
            "nome": dispositivo.nome,
            "descricao": dispositivo.descricao,
            "chave": dispositivo.chave,
            "ativo": dispositivo.ativo
        })
    except DispositivoNaoEncontrado:
        return jsonify({"erro": "Dispositivo nao encontrado"}), 404


@dispositivo_bp.route('/dispositivos/<chave>', methods=['DELETE'])
@cross_origin(origin='*')
def deletar(chave):
    usuario = AutenticacaoService.instancia().obter_usuario_autenticado()
    if not usuario:
        return jsonify({"erro": "Token invalido ou ausente"}), 401

    try:
        dispositivo = DispositivoService.instancia().buscar_por_chave(chave)
        if dispositivo.usuario_id != usuario.id:
            return jsonify({"erro": "Dispositivo nao pertence a este usuario"}), 403
        DispositivoService.instancia().deletar(dispositivo)
        return jsonify({"mensagem": "Dispositivo deletado"}), 200
    except DispositivoNaoEncontrado:
        return jsonify({"erro": "Dispositivo nao encontrado"}), 404
