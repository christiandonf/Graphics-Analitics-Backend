import os
from flask import Flask
from flask_cors import CORS
from database import db
from controller.usuario_controller import usuario_bp
from controller.dispositivo_controller import dispositivo_bp
from controller.leitura_controller import leitura_bp
from controller.grafico_controller import grafico_bp

host = str(os.environ.get("HOST", "localhost"))
port = int(os.environ.get("PORT", 5000))
debug = str(os.environ.get("DEBUG", "true"))

db_user = str(os.environ.get("POSTGRES_USER_KEY", "postgres"))
db_port = str(os.environ.get("POSTGRES_PORT_KEY", "5432"))
db_host = str(os.environ.get("POSTGRES_HOST_KEY", "localhost"))
db_password = str(os.environ.get("POSTGRES_PASSWORD_KEY", "123456789"))

app = Flask(__name__)
CORS(
    app,
    supports_credentials=True,
    resources={r"/api/*": {"origins": "http://analitics.nexuswebdigital.com"}},
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql+psycopg2://%s:%s@%s:%s/graphics_analytics' %(db_user, db_password, db_host, db_port)
)

db.init_app(app)
app.register_blueprint(usuario_bp)
app.register_blueprint(dispositivo_bp)
app.register_blueprint(leitura_bp)
app.register_blueprint(grafico_bp)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=debug, port=port, host=host)
