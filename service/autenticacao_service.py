from flask import request
from dao.usuario_dao import UsuarioDao


class AutenticacaoService:
    _instancia = None

    @classmethod
    def instancia(cls):
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def __init__(self):
        self.dao = UsuarioDao.instancia()

    def obter_usuario_autenticado(self):
        token = request.headers.get('Authorization')
        if not token:
            return None
        usuario = self.dao.buscar_por_token(token)
        return usuario
