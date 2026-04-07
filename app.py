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
    app.run(debug=True)
