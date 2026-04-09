import os
from flask import Flask
from database import db
from controller.usuario_controller import usuario_bp
from controller.dispositivo_controller import dispositivo_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///graphics_analytics.db'

db.init_app(app)
app.register_blueprint(usuario_bp)
app.register_blueprint(dispositivo_bp)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    host = str(os.environ.get("HOST", "localhost"))
    port = int(os.environ.get("PORT", 5000))
    debug = str(os.environ.get("DEBUG", "true"))
    app.run(debug=debug, port=port, host=host)
