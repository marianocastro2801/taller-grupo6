from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()


def init_app(app):
    db.init_app(app)
    config_db(app)


def config_db(app):
    app.config.from_object(Config)

    @app.before_first_request
    def init_database():
        db.create_all()  # a partir de los modelos crea las tablas

    @app.teardown_request
    def close_session(exception=None):
        db.session.remove()  # cierra la sesión
