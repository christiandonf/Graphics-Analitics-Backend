from model.leitura import Leitura, LeituraNaoEncontrada
from dao.leitura_dao import LeituraDao


PERIODOS_VALIDOS = ('hora', 'dia', 'mes', 'ano')


class PeriodoInvalido(Exception):
    pass


class LeituraService:
    _instancia = None

    @classmethod
    def instancia(cls):
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def __init__(self):
        self.dao = LeituraDao.instancia()

    def criar(self, dispositivo_id, payload):
        leitura = Leitura(dispositivo_id=dispositivo_id, payload=payload)
        return self.dao.criar(leitura)

    def listar(self, dispositivo_id, desde=None, ate=None, limite=100):
        return self.dao.listar_por_dispositivo(dispositivo_id, desde, ate, limite)

    def estatisticas(self, dispositivo_id, campo):
        leituras = self.dao.listar_por_dispositivo(dispositivo_id, limite=None)
        valores = self._valores_numericos(leituras, campo)

        if not valores:
            raise LeituraNaoEncontrada()

        return {
            "campo": campo,
            "contagem": len(valores),
            "minimo": min(valores),
            "maximo": max(valores),
            "media": round(sum(valores) / len(valores), 2)
        }

    def agrupar_por_periodo(self, dispositivo_id, campo, periodo, desde=None, ate=None):
        if periodo not in PERIODOS_VALIDOS:
            raise PeriodoInvalido()

        leituras = self.dao.listar_por_dispositivo(
            dispositivo_id, desde=desde, ate=ate, limite=None
        )

        grupos = {}
        for leitura in leituras:
            valor = leitura.payload.get(campo)
            if not isinstance(valor, (int, float)):
                continue
            chave = self._truncar_data(leitura.criado_em, periodo)
            grupos.setdefault(chave, []).append(valor)

        if not grupos:
            raise LeituraNaoEncontrada()

        resultado = []
        for chave in sorted(grupos.keys()):
            valores = grupos[chave]
            resultado.append({
                "periodo": chave,
                "contagem": len(valores),
                "minimo": min(valores),
                "maximo": max(valores),
                "media": round(sum(valores) / len(valores), 2)
            })
        return {"campo": campo, "agrupamento": periodo, "pontos": resultado}

    def _valores_numericos(self, leituras, campo):
        return [
            l.payload[campo] for l in leituras
            if campo in l.payload and isinstance(l.payload[campo], (int, float))
        ]

    def _truncar_data(self, dt, periodo):
        if periodo == 'hora':
            return dt.strftime('%Y-%m-%dT%H:00')
        if periodo == 'dia':
            return dt.strftime('%Y-%m-%d')
        if periodo == 'mes':
            return dt.strftime('%Y-%m')
        return dt.strftime('%Y')
