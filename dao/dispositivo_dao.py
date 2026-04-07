from model.dispositivo import Dispositivo
from database import db


class DispositivoDao:
    _instancia = None

    @classmethod
    def instancia(cls):
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def criar(self, dispositivo):
        db.session.add(dispositivo)
        db.session.commit()
        return dispositivo

    def buscar_por_id(self, id):
        return db.session.get(Dispositivo, id)

    def buscar_por_chave(self, chave):
        return Dispositivo.query.filter_by(chave=chave).first()

    def listar_por_usuario(self, usuario_id):
        return Dispositivo.query.filter_by(usuario_id=usuario_id).all()

    def deletar(self, dispositivo):
        db.session.delete(dispositivo)
        db.session.commit()
