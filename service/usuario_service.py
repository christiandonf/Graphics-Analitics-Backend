import re
from model.usuario import (
    Usuario,
    UsuarioNaoEncontrado,
    EmailJaCadastrado,
    SenhaInvalida,
    EmailInvalido,
    SenhaMuitoCurta,
    NomeInvalido,
)
from dao.usuario_dao import UsuarioDao
import bcrypt


REGEX_EMAIL = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')
SENHA_MINIMA = 6
NOME_MINIMO = 2


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
        self._validar_nome(nome)
        self._validar_email(email)
        self._validar_senha(senha)

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

    def login(self, email, senha):
        usuario = self.dao.buscar_por_email(email)
        if not usuario:
            raise UsuarioNaoEncontrado()

        senha_correta = bcrypt.checkpw(
            senha.encode('utf-8'),
            usuario.senha_hash.encode('utf-8')
        )
        if not senha_correta:
            raise SenhaInvalida()

        return usuario

    def atualizar(self, usuario, nome=None, email=None, senha=None):
        if nome is not None:
            self._validar_nome(nome)
            usuario.nome = nome
        if email is not None and email != usuario.email:
            self._validar_email(email)
            if self.dao.buscar_por_email(email):
                raise EmailJaCadastrado()
            usuario.email = email
        if senha is not None:
            self._validar_senha(senha)
            usuario.senha_hash = bcrypt.hashpw(
                senha.encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')
        return self.dao.atualizar(usuario)

    def _validar_nome(self, nome):
        if not isinstance(nome, str) or len(nome.strip()) < NOME_MINIMO:
            raise NomeInvalido()

    def _validar_email(self, email):
        if not isinstance(email, str) or not REGEX_EMAIL.match(email):
            raise EmailInvalido()

    def _validar_senha(self, senha):
        if not isinstance(senha, str) or len(senha) < SENHA_MINIMA:
            raise SenhaMuitoCurta()
