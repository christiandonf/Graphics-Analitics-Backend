from database import db
from datetime import datetime
import uuid

class UsuarioNaoEncontrado(Exception):
    pass


class EmailJaCadastrado(Exception):
    pass


class SenhaInvalida(Exception):
    pass


class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    token_api = db.Column(db.String(36), unique=True, default=lambda: str(uuid.uuid4()))
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
