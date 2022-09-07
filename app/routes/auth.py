from flask import Blueprint, request
from app.resources import auth

authentication = Blueprint('auth', __name__)

authentication.add_url_rule("/iniciar_sesion", "login", auth.login)
authentication.add_url_rule("/cerrar_sesion", "logout", auth.logout)
authentication.add_url_rule(
        "/autenticacion", "authenticate", auth.authenticate, methods=["POST"]
    )