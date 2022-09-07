from os import environ
from flask import Flask, render_template, request
from flask_session import Session
from config import config
from app import db
from app.helpers import handler
from app.helpers import auth as helper_auth
from app.helpers import verifications as helper_verifications
from flask_fontawesome import FontAwesome
from .routes.users import users
from .routes.auth import authentication
from .routes.home import home


def create_app(environment="production"):
    # Configuración inicial de la app
    app = Flask(__name__)
    fa = FontAwesome(app)

    # Carga de la configuración
    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])

    # Server Side session
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Configure db
    db.init_app(app)

    # Funciones que se exportan al contexto de Jinja2
    app.jinja_env.globals.update(
        is_authenticated=helper_auth.authenticated,
        user_has_permission=helper_verifications.user_has_permission
    )

    # Autenticación
    app.register_blueprint(authentication)

    # Usuarios
    app.register_blueprint(users)


    # Ruta para el Home
    app.register_blueprint(home)

    # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)
    app.register_error_handler(500, handler.internal_error_error)

    # Retornar la instancia de app configurada
    return app
