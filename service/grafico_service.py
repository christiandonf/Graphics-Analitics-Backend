from model.grafico import Grafico, GraficoNaoEncontrado, TipoGraficoInvalido
from model.leitura import LeituraNaoEncontrada
from dao.grafico_dao import GraficoDao
from service.leitura_service import LeituraService, PERIODOS_VALIDOS, PeriodoInvalido


TIPOS_VALIDOS = ('linha', 'barra', 'area', 'pizza')
FAIXAS_PIZZA = 4
LIMITE_PONTOS_BRUTOS = 200


class GraficoService:
    _instancia = None

    @classmethod
    def instancia(cls):
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def __init__(self):
        self.dao = GraficoDao.instancia()
        self.leitura_service = LeituraService.instancia()

    def criar(self, usuario_id, dispositivo_id, nome, campo, tipo, periodo=None, favorito=False):
        self._validar_tipo(tipo)
        if periodo is not None:
            self._validar_periodo(periodo)

        grafico = Grafico(
            usuario_id=usuario_id,
            dispositivo_id=dispositivo_id,
            nome=nome,
            campo=campo,
            tipo=tipo,
            periodo=periodo,
            favorito=bool(favorito)
        )
        return self.dao.criar(grafico)

    def buscar(self, id):
        grafico = self.dao.buscar_por_id(id)
        if not grafico:
            raise GraficoNaoEncontrado()
        return grafico

    def listar_por_usuario(self, usuario_id):
        return self.dao.listar_por_usuario(usuario_id)

    def listar_favoritos(self, usuario_id):
        return self.dao.listar_favoritos(usuario_id)

    def atualizar(self, grafico, nome=None, campo=None, tipo=None, periodo=None, favorito=None):
        if tipo is not None:
            self._validar_tipo(tipo)
            grafico.tipo = tipo
        if periodo is not None:
            self._validar_periodo(periodo)
            grafico.periodo = periodo
        if nome is not None:
            grafico.nome = nome
        if campo is not None:
            grafico.campo = campo
        if favorito is not None:
            grafico.favorito = bool(favorito)
        return self.dao.atualizar(grafico)

    def deletar(self, grafico):
        self.dao.deletar(grafico)

    def gerar_dados(self, grafico):
        if grafico.tipo == 'pizza':
            return self._gerar_pizza(grafico)
        return self._gerar_serie(grafico)

    def _gerar_serie(self, grafico):
        if grafico.periodo:
            try:
                resultado = self.leitura_service.agrupar_por_periodo(
                    grafico.dispositivo_id, grafico.campo, grafico.periodo
                )
                pontos = resultado['pontos']
                return {
                    'labels': [p['periodo'] for p in pontos],
                    'valores': [p['media'] for p in pontos]
                }
            except LeituraNaoEncontrada:
                return {'labels': [], 'valores': []}

        leituras = self.leitura_service.listar(
            grafico.dispositivo_id, limite=LIMITE_PONTOS_BRUTOS
        )
        leituras = list(reversed(leituras))
        labels = []
        valores = []
        for l in leituras:
            valor = l.payload.get(grafico.campo)
            if isinstance(valor, (int, float)):
                labels.append(l.criado_em.isoformat())
                valores.append(valor)
        return {'labels': labels, 'valores': valores}

    def _gerar_pizza(self, grafico):
        leituras = self.leitura_service.listar(grafico.dispositivo_id, limite=None)
        valores = [
            l.payload[grafico.campo] for l in leituras
            if grafico.campo in l.payload and isinstance(l.payload[grafico.campo], (int, float))
        ]
        if not valores:
            return {'labels': [], 'valores': []}

        minimo = min(valores)
        maximo = max(valores)
        if minimo == maximo:
            return {'labels': [str(minimo)], 'valores': [len(valores)]}

        passo = (maximo - minimo) / FAIXAS_PIZZA
        buckets = [0] * FAIXAS_PIZZA
        labels = [
            f'{round(minimo + i * passo, 2)} - {round(minimo + (i + 1) * passo, 2)}'
            for i in range(FAIXAS_PIZZA)
        ]
        for v in valores:
            idx = min(int((v - minimo) / passo), FAIXAS_PIZZA - 1)
            buckets[idx] += 1
        return {'labels': labels, 'valores': buckets}

    def _validar_tipo(self, tipo):
        if tipo not in TIPOS_VALIDOS:
            raise TipoGraficoInvalido()

    def _validar_periodo(self, periodo):
        if periodo not in PERIODOS_VALIDOS:
            raise PeriodoInvalido()
