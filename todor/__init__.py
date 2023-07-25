from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)

    # ! CONFIGURACIÓN DEL PROYECTO. !
    app.config.from_mapping(
        DEBUG=True,  # * DEBUG A TRUE
        SECRET_KEY='dev',  # * LLAVE SECRETA PARA LOS FORMULARIOS
        SQLALCHEMY_DATABASE_URI="sqlite:///todolist.db" # * AGREGAMOS EL NOMBRE A LA BASE DE DATOS
    )

    # * INICIALIZAMOS SQLALCHEMY
    db.init_app(app)

    # ! REGISTRAMOS BLUEPRINT !
    from todor import todo
    app.register_blueprint(todo.bp)

    from todor import auth
    app.register_blueprint(auth.bp)

    @app.route('/')
    def index():
        return render_template('index.html')
    
    # * MIGRAMOS LOS MODELOS SQLALCHEMY A LA BASE DE DATOS
    with app.app_context():
        db.create_all()

    return app
