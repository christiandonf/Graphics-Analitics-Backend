from database import db
from datetime import datetime, timezone


class GraficoNaoEncontrado(Exception):
    pass


class TipoGraficoInvalido(Exception):
    pass


class CampoGraficoInvalido(Exception):
    pass


class Grafico(db.Model):
    __tablename__ = 'graficos'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    dispositivo_id = db.Column(db.Integer, db.ForeignKey('dispositivos.id', ondelete='CASCADE'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    campo = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    periodo = db.Column(db.String(10))
    favorito = db.Column(db.Boolean, default=False, nullable=False)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
