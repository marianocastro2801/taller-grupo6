from email.policy import default
from flask import Blueprint, request, render_template, session, redirect, url_for, abort 
from app.resources import vacunattion
from app.resources import vacunattionApi

from app.helpers.verifications import user_has_permission
from app.helpers.auth import authenticated

vacunattionesApi = Blueprint('vacunattionesApi', __name__)


vacunattionesApi.add_url_rule("/vacunaciones/nueva_vacunacion", "nueva_vacunacion", vacunattionApi.new_con_api)
vacunattionesApi.add_url_rule("/vacunaciones/vacunattion_save_api", "vacunattion_save_api", vacunattionApi.save_con_api, methods=["POST"])