from flask import Blueprint, request, jsonify
from service.dispositivo_service import DispositivoService
from model.dispositivo import DispositivoNaoEncontrado

dispositivo_bp = Blueprint('dispositivo', __name__)


@dispositivo_bp.route('/dispositivos', methods=['POST'])
def criar():
    dados = request.get_json()
    dispositivo = DispositivoService.instancia().criar(
        usuario_id=dados['usuario_id'],
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


@dispositivo_bp.route('/dispositivos/<int:usuario_id>', methods=['GET'])
def listar(usuario_id):
    dispositivos = DispositivoService.instancia().listar_por_usuario(usuario_id)
    return jsonify([{
        "id": d.id,
        "nome": d.nome,
        "descricao": d.descricao,
        "chave": d.chave,
        "ativo": d.ativo
    } for d in dispositivos])


@dispositivo_bp.route('/dispositivos/<int:id>', methods=['DELETE'])
def deletar(id):
    try:
        DispositivoService.instancia().deletar(id)
        return jsonify({"mensagem": "Dispositivo deletado"}), 200
    except DispositivoNaoEncontrado:
        return jsonify({"erro": "Dispositivo nao encontrado"}), 404
