from model.dispositivo import Dispositivo, DispositivoNaoEncontrado
from dao.dispositivo_dao import DispositivoDao


class DispositivoService:
    _instancia = None

    @classmethod
    def instancia(cls):
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def __init__(self):
        self.dao = DispositivoDao.instancia()

    def criar(self, usuario_id, nome, descricao=None):
        dispositivo = Dispositivo(usuario_id=usuario_id, nome=nome, descricao=descricao)
        return self.dao.criar(dispositivo)

    def buscar_por_id(self, id):
        dispositivo = self.dao.buscar_por_id(id)
        if not dispositivo:
            raise DispositivoNaoEncontrado()
        return dispositivo

    def buscar_por_chave(self, chave):
        dispositivo = self.dao.buscar_por_chave(chave)
        if not dispositivo:
            raise DispositivoNaoEncontrado()
        return dispositivo

    def listar_por_usuario(self, usuario_id):
        return self.dao.listar_por_usuario(usuario_id)

    def atualizar(self, dispositivo, nome=None, descricao=None, ativo=None):
        if nome is not None:
            dispositivo.nome = nome
        if descricao is not None:
            dispositivo.descricao = descricao
        if ativo is not None:
            dispositivo.ativo = ativo
        return self.dao.atualizar(dispositivo)

    def deletar(self, dispositivo):
        self.dao.deletar(dispositivo)
