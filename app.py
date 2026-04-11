import os
from flask import Flask
from database import db
from controller.usuario_controller import usuario_bp
from controller.dispositivo_controller import dispositivo_bp

# Variaveis dinamicas que sao usadas para definir qual a porta do servidor e o host do mesmo
host = str(os.environ.get("HOST", "localhost"))
port = int(os.environ.get("PORT", 5000))
debug = str(os.environ.get("DEBUG", "true"))

# Variaveis dinamicas usadas para definir o Host do banco de dados assim conectando a banco de dados dedicado
db_user = str(os.environ.get("POSTGRES_DB_KEY", "fauUser"))
db_name = str(os.environ.get("POSTGRES_USER_KEY", "facu"))
db_host = str(os.environ.get("POSTGRES_HOST_KEY", "127.0.0.1"))
db_password = int(os.environ.get("POSTGRES_PASSWORD_KEY", 123456789))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///graphics_analytics.db'

db.init_app(app)
app.register_blueprint(usuario_bp)
app.register_blueprint(dispositivo_bp)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=debug, port=port, host=host)
