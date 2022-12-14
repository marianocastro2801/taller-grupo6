from os import environ
from flask import Flask, Blueprint
from flask import Flask, render_template, request
from flask_session import Session
from config import config
from app import db
from app.helpers import handler
from app.helpers import auth as helper_auth
from app.helpers import verifications as helper_verifications
from flask_fontawesome import FontAwesome
from .routes.users import users
from .routes.vaccines import vaccines
from .routes.shopping import shoppings
from .routes.distributtiones import distributtiones
from .routes.patology import patologys
from .routes.vacunattiones import vacunattiones
from .routes.auth import authentication
from .routes.home import home
from app.resources.api import vacunados
from app.resources.api import vacunados_por_vacuna_desarrollada
from app.resources.api import vacunados_por_provincia
# from .api.persona import persona_api


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

    # Vacunas
    app.register_blueprint(vaccines)

    # Compras de vacunas
    app.register_blueprint(shoppings)

    # Distribuciones
    app.register_blueprint(distributtiones)
    
    # Patologias/vacunas para
    app.register_blueprint(patologys)

    # Vacunaciones
    app.register_blueprint(vacunattiones)

    # Ruta para el Home
    app.register_blueprint(home)

    # Rutas de API-REST   
    app.add_url_rule('/api/vacunaciones', 'mostrar_vacunaciones',vacunados.mostrar_vacunaciones, methods=['GET'])
    app.add_url_rule('/api/vacunaciones_por_vacuna_desarrolladora/<int:id>', 'mostrar_vacunaciones_por_vacuna_desarrolladora',vacunados_por_vacuna_desarrollada.mostrar_vacunacion_por_vd, methods=['GET'])
    app.add_url_rule('/api/vacunaciones_por_provincia/<int:id>', 'mostrar_vacunaciones_por_provincia',vacunados_por_provincia.mostrar_vacunacion_por_provincia, methods=['GET'])
    app.add_url_rule('/api/crear_vacunaciones', 'crear_vacunaciones',vacunados.crear_vacunaciones, methods=['GET'])
    # api = Blueprint("api", __name__, url_prefix="/api")
    # api.register_blueprint(persona_api) 



    # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)
    app.register_error_handler(500, handler.internal_error_error)

    # Retornar la instancia de app configurada
    return app
