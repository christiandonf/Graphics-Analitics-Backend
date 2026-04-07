from database import db
from datetime import datetime
import uuid


class DispositivoNaoEncontrado(Exception):
    pass


class Dispositivo(db.Model):
    __tablename__ = 'dispositivos'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200))
    chave = db.Column(db.String(36), unique=True, default=lambda: str(uuid.uuid4()), nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
