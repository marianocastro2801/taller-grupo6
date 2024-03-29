from email.policy import default
from flask import Blueprint, request
from app.resources import vacunattion
from app.resources import vacunattionApi

from app.helpers.verifications import user_has_permission
from app.helpers.auth import authenticated

vacunattiones = Blueprint('vacunattiones', __name__)


vacunattiones.add_url_rule("/vacunaciones/vacunattion_new", "vacunattion_new", vacunattion.new)
vacunattiones.add_url_rule("/vacunaciones/vacunattion_save", "vacunattion_save", vacunattion.save, methods=["POST"])


#@vacunattiones.route('/vacunaciones/vacunattion_index/<int:provincia_id>')
@vacunattiones.route('/vacunaciones/vacunattion_index')
def vacunattion_index():

    enfermedad_id = request.args.get('enfermedad_id', '2')

    return vacunattion.index(enfermedad_id)


vacunattiones.add_url_rule("/vacunaciones/vacunacion/<int:vacunattion_id>", "vacunattion_profile", vacunattion.profile)

vacunattiones.add_url_rule("/vacunaciones/vacunattion_etl", "vacunattion_etl", vacunattion.etl)