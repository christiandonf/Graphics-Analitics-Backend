from model.leitura import Leitura, LeituraNaoEncontrada
from dao.leitura_dao import LeituraDao


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
        leituras = self.dao.listar_por_dispositivo(dispositivo_id)

        valores = [
            l.payload[campo] for l in leituras
            if campo in l.payload and isinstance(l.payload[campo], (int, float))
        ]

        if not valores:
            raise LeituraNaoEncontrada()

        return {
            "campo": campo,
            "contagem": len(valores),
            "minimo": min(valores),
            "maximo": max(valores),
            "media": round(sum(valores) / len(valores), 2)
        }
