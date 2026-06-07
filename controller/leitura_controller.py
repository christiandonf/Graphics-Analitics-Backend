from flask import Blueprint, request, jsonify
from service.leitura_service import LeituraService, PeriodoInvalido
from service.dispositivo_service import DispositivoService
from service.autenticacao_service import AutenticacaoService
from model.dispositivo import DispositivoNaoEncontrado
from model.leitura import LeituraNaoEncontrada
from datetime import datetime

leitura_bp = Blueprint('leitura', __name__)


@leitura_bp.route('/feed/<chave>', methods=['POST'])
def enviar(chave):
    try:
        dispositivo = DispositivoService.instancia().buscar_por_chave(chave)
    except DispositivoNaoEncontrado:
        return jsonify({"erro": "Dispositivo nao encontrado"}), 404

    payload = request.args.to_dict()

    if not payload:
        return jsonify({"erro": "Nenhum dado enviado"}), 400

    for chave_param, valor in payload.items():
        try:
            payload[chave_param] = float(valor)
        except ValueError:
            pass

    leitura = LeituraService.instancia().criar(dispositivo.id, payload)
    return jsonify({
        "mensagem": "Dado recebido",
        "payload": leitura.payload,
        "criado_em": leitura.criado_em.isoformat()
    }), 201


@leitura_bp.route('/dados/<chave>', methods=['GET'])
def listar(chave):
    usuario = AutenticacaoService.instancia().obter_usuario_autenticado()
    if not usuario:
        return jsonify({"erro": "Token invalido ou ausente"}), 401

    try:
        dispositivo = DispositivoService.instancia().buscar_por_chave(chave)
    except DispositivoNaoEncontrado:
        return jsonify({"erro": "Dispositivo nao encontrado"}), 404

    if dispositivo.usuario_id != usuario.id:
        return jsonify({"erro": "Dispositivo nao pertence a este usuario"}), 403

    desde, ate, erro = _parse_intervalo()
    if erro:
        return erro
    limite = request.args.get('limite', 100, type=int)

    leituras = LeituraService.instancia().listar(dispositivo.id, desde, ate, limite)
    return jsonify([{
        "id": l.id,
        "payload": l.payload,
        "criado_em": l.criado_em.isoformat()
    } for l in leituras])


@leitura_bp.route('/estatisticas/<chave>/<campo>', methods=['GET'])
def estatisticas(chave, campo):
    usuario = AutenticacaoService.instancia().obter_usuario_autenticado()
    if not usuario:
        return jsonify({"erro": "Token invalido ou ausente"}), 401

    try:
        dispositivo = DispositivoService.instancia().buscar_por_chave(chave)
    except DispositivoNaoEncontrado:
        return jsonify({"erro": "Dispositivo nao encontrado"}), 404

    if dispositivo.usuario_id != usuario.id:
        return jsonify({"erro": "Dispositivo nao pertence a este usuario"}), 403

    try:
        stats = LeituraService.instancia().estatisticas(dispositivo.id, campo)
        return jsonify(stats)
    except LeituraNaoEncontrada:
        return jsonify({"erro": "Nenhum dado encontrado para esse campo"}), 404


@leitura_bp.route('/agrupamento/<chave>/<campo>', methods=['GET'])
def agrupamento(chave, campo):
    usuario = AutenticacaoService.instancia().obter_usuario_autenticado()
    if not usuario:
        return jsonify({"erro": "Token invalido ou ausente"}), 401

    try:
        dispositivo = DispositivoService.instancia().buscar_por_chave(chave)
    except DispositivoNaoEncontrado:
        return jsonify({"erro": "Dispositivo nao encontrado"}), 404

    if dispositivo.usuario_id != usuario.id:
        return jsonify({"erro": "Dispositivo nao pertence a este usuario"}), 403

    periodo = request.args.get('periodo', 'dia')
    desde, ate, erro = _parse_intervalo()
    if erro:
        return erro

    try:
        resultado = LeituraService.instancia().agrupar_por_periodo(
            dispositivo.id, campo, periodo, desde, ate
        )
        return jsonify(resultado)
    except PeriodoInvalido:
        return jsonify({"erro": "Periodo invalido (use hora, dia, mes ou ano)"}), 400
    except LeituraNaoEncontrada:
        return jsonify({"erro": "Nenhum dado encontrado para esse campo"}), 404


def _parse_intervalo():
    desde = request.args.get('desde')
    ate = request.args.get('ate')
    try:
        if desde:
            desde = datetime.fromisoformat(desde)
        if ate:
            ate = datetime.fromisoformat(ate)
    except ValueError:
        return None, None, (jsonify({"erro": "Formato de data invalido (use ISO 8601)"}), 400)
    return desde, ate, None
