from flask import Blueprint, request, jsonify
from service.grafico_service import GraficoService
from service.dispositivo_service import DispositivoService
from service.autenticacao_service import AutenticacaoService
from service.leitura_service import PeriodoInvalido
from model.grafico import GraficoNaoEncontrado, TipoGraficoInvalido
from model.dispositivo import DispositivoNaoEncontrado

grafico_bp = Blueprint('grafico', __name__)


@grafico_bp.route('/graficos', methods=['POST'])
def criar():
    usuario = AutenticacaoService.instancia().obter_usuario_autenticado()
    if not usuario:
        return jsonify({"erro": "Token invalido ou ausente"}), 401

    dados = request.get_json()

    try:
        dispositivo = DispositivoService.instancia().buscar_por_chave(dados['dispositivo_chave'])
    except DispositivoNaoEncontrado:
        return jsonify({"erro": "Dispositivo nao encontrado"}), 404

    if dispositivo.usuario_id != usuario.id:
        return jsonify({"erro": "Dispositivo nao pertence a este usuario"}), 403

    try:
        grafico = GraficoService.instancia().criar(
            usuario_id=usuario.id,
            dispositivo_id=dispositivo.id,
            nome=dados['nome'],
            campo=dados['campo'],
            tipo=dados['tipo'],
            periodo=dados.get('periodo'),
            favorito=dados.get('favorito', False)
        )
        return jsonify(_serializar(grafico, dispositivo)), 201
    except TipoGraficoInvalido:
        return jsonify({"erro": "Tipo invalido (use linha, barra, area ou pizza)"}), 400
    except PeriodoInvalido:
        return jsonify({"erro": "Periodo invalido (use hora, dia, mes ou ano)"}), 400


@grafico_bp.route('/graficos', methods=['GET'])
def listar():
    usuario = AutenticacaoService.instancia().obter_usuario_autenticado()
    if not usuario:
        return jsonify({"erro": "Token invalido ou ausente"}), 401

    apenas_favoritos = request.args.get('favoritos') == 'true'
    if apenas_favoritos:
        graficos = GraficoService.instancia().listar_favoritos(usuario.id)
    else:
        graficos = GraficoService.instancia().listar_por_usuario(usuario.id)

    resultado = []
    for g in graficos:
        dispositivo = DispositivoService.instancia().buscar_por_id(g.dispositivo_id)
        resultado.append(_serializar(g, dispositivo))
    return jsonify(resultado)


@grafico_bp.route('/graficos/<int:id>', methods=['GET'])
def buscar(id):
    usuario = AutenticacaoService.instancia().obter_usuario_autenticado()
    if not usuario:
        return jsonify({"erro": "Token invalido ou ausente"}), 401

    try:
        grafico = GraficoService.instancia().buscar(id)
    except GraficoNaoEncontrado:
        return jsonify({"erro": "Grafico nao encontrado"}), 404

    if grafico.usuario_id != usuario.id:
        return jsonify({"erro": "Grafico nao pertence a este usuario"}), 403

    dispositivo = DispositivoService.instancia().buscar_por_id(grafico.dispositivo_id)
    dados = GraficoService.instancia().gerar_dados(grafico)
    return jsonify({
        **_serializar(grafico, dispositivo),
        "dados": dados
    })


@grafico_bp.route('/graficos/<int:id>', methods=['PUT'])
def atualizar(id):
    usuario = AutenticacaoService.instancia().obter_usuario_autenticado()
    if not usuario:
        return jsonify({"erro": "Token invalido ou ausente"}), 401

    try:
        grafico = GraficoService.instancia().buscar(id)
    except GraficoNaoEncontrado:
        return jsonify({"erro": "Grafico nao encontrado"}), 404

    if grafico.usuario_id != usuario.id:
        return jsonify({"erro": "Grafico nao pertence a este usuario"}), 403

    dados = request.get_json()
    try:
        grafico = GraficoService.instancia().atualizar(
            grafico,
            nome=dados.get('nome'),
            campo=dados.get('campo'),
            tipo=dados.get('tipo'),
            periodo=dados.get('periodo'),
            favorito=dados.get('favorito')
        )
        dispositivo = DispositivoService.instancia().buscar_por_id(grafico.dispositivo_id)
        return jsonify(_serializar(grafico, dispositivo))
    except TipoGraficoInvalido:
        return jsonify({"erro": "Tipo invalido (use linha, barra, area ou pizza)"}), 400
    except PeriodoInvalido:
        return jsonify({"erro": "Periodo invalido (use hora, dia, mes ou ano)"}), 400


@grafico_bp.route('/graficos/<int:id>', methods=['DELETE'])
def deletar(id):
    usuario = AutenticacaoService.instancia().obter_usuario_autenticado()
    if not usuario:
        return jsonify({"erro": "Token invalido ou ausente"}), 401

    try:
        grafico = GraficoService.instancia().buscar(id)
    except GraficoNaoEncontrado:
        return jsonify({"erro": "Grafico nao encontrado"}), 404

    if grafico.usuario_id != usuario.id:
        return jsonify({"erro": "Grafico nao pertence a este usuario"}), 403

    GraficoService.instancia().deletar(grafico)
    return jsonify({"mensagem": "Grafico deletado"}), 200


def _serializar(grafico, dispositivo):
    return {
        "id": grafico.id,
        "nome": grafico.nome,
        "dispositivo_chave": dispositivo.chave,
        "dispositivo_nome": dispositivo.nome,
        "campo": grafico.campo,
        "tipo": grafico.tipo,
        "periodo": grafico.periodo,
        "favorito": grafico.favorito
    }
