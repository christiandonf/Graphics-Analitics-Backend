import os
from flask import Flask
from database import db
from controller.usuario_controller import usuario_bp
from controller.dispositivo_controller import dispositivo_bp
from controller.leitura_controller import leitura_bp
import os

host = str(os.environ.get("HOST", "localhost"))
port = int(os.environ.get("PORT", 5000))
debug = str(os.environ.get("DEBUG", "true"))

db_user = str(os.environ.get("POSTGRES_DB_KEY", "fauUser"))
db_name = str(os.environ.get("POSTGRES_USER_KEY", "facu"))
db_host = str(os.environ.get("POSTGRES_HOST_KEY", "127.0.0.1"))
db_password = int(os.environ.get("POSTGRES_PASSWORD_KEY", 123456789))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql://postgres:postgres@localhost:5432/graphics_analytics'
)

db.init_app(app)
app.register_blueprint(usuario_bp)
app.register_blueprint(dispositivo_bp)
app.register_blueprint(leitura_bp)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=debug, port=port, host=host)
