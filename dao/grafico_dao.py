from model.grafico import Grafico
from database import db


class GraficoDao:
    _instancia = None

    @classmethod
    def instancia(cls):
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def criar(self, grafico):
        db.session.add(grafico)
        db.session.commit()
        return grafico

    def atualizar(self, grafico):
        db.session.commit()
        return grafico

    def buscar_por_id(self, id):
        return db.session.get(Grafico, id)

    def listar_por_usuario(self, usuario_id):
        return Grafico.query.filter_by(usuario_id=usuario_id).all()

    def listar_favoritos(self, usuario_id):
        return Grafico.query.filter_by(usuario_id=usuario_id, favorito=True).all()

    def deletar(self, grafico):
        db.session.delete(grafico)
        db.session.commit()
