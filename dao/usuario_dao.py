from model.usuario import Usuario
from database import db


class UsuarioDao:
    _instancia = None

    @classmethod
    def instancia(cls):
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def criar(self, usuario):
        db.session.add(usuario)
        db.session.commit()
        return usuario

    def buscar_por_id(self, id):
        return db.session.get(Usuario, id)

    def buscar_por_email(self, email):
        return Usuario.query.filter_by(email=email).first()

    def buscar_por_token(self, token_api):
        return Usuario.query.filter_by(token_api=token_api).first()
