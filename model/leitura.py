from database import db
from datetime import datetime, timezone


class LeituraNaoEncontrada(Exception):
    pass


class Leitura(db.Model):
    __tablename__ = 'leituras'

    id = db.Column(db.Integer, primary_key=True)
    dispositivo_id = db.Column(db.Integer, db.ForeignKey('dispositivos.id'), nullable=False)
    payload = db.Column(db.JSON, nullable=False)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
