from model.leitura import Leitura
from database import db


class LeituraDao:
    _instancia = None

    @classmethod
    def instancia(cls):
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def criar(self, leitura):
        db.session.add(leitura)
        db.session.commit()
        return leitura

    def listar_por_dispositivo(self, dispositivo_id, desde=None, ate=None, limite=100):
        query = Leitura.query.filter_by(dispositivo_id=dispositivo_id)

        if desde:
            query = query.filter(Leitura.criado_em >= desde)
        if ate:
            query = query.filter(Leitura.criado_em <= ate)

        return query.order_by(Leitura.criado_em.desc()).limit(limite).all()
