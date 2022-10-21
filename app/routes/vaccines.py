from asyncio.windows_events import NULL
from contextlib import nullcontext
from email.policy import default
from flask import Blueprint, request
from app.resources import vaccine

vaccines = Blueprint('vaccines', __name__)


vaccines.add_url_rule("/vacunas/vaccine_new", "vaccine_new", vaccine.new)
vaccines.add_url_rule("/vacunas/vaccine_save", "vaccine_save", vaccine.save, methods=["POST"])
vaccines.add_url_rule("/vacunas/vaccine_update", "vaccine_update", vaccine.update, methods=["POST"])
vaccines.add_url_rule("/vacunas/vaccine_delete/<int:vaccine_id>", "vaccine_delete", vaccine.delete)

@vaccines.route('/vacunas/editar/<int:vaccine_id>')
def vaccine_edit(vaccine_id):
    return vaccine.edit(vaccine_id)


@vaccines.route('/vacunas/vaccine_index')
@vaccines.route('/vacunas/vaccine_index')
def vaccine_index():
    
    type_id = request.args.get('type_id', '2')
    search = request.args.get('search', '')

    return vaccine.index(search, type_id)





