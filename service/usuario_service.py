from model.usuario import Usuario, UsuarioNaoEncontrado, EmailJaCadastrado
from dao.usuario_dao import UsuarioDao
import bcrypt


class UsuarioService:
    _instancia = None

    @classmethod
    def instancia(cls):
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def __init__(self):
        self.dao = UsuarioDao.instancia()

    def registrar(self, nome, email, senha):
        if self.dao.buscar_por_email(email):
            raise EmailJaCadastrado()

        senha_hash = bcrypt.hashpw(
            senha.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        usuario = Usuario(nome=nome, email=email, senha_hash=senha_hash)
        return self.dao.criar(usuario)

    def buscar_por_id(self, id):
        usuario = self.dao.buscar_por_id(id)
        if not usuario:
            raise UsuarioNaoEncontrado()
        return usuario
