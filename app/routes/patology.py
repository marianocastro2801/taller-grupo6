from email.policy import default
from flask import Blueprint, request, session, render_template
from app.resources import patology


patologys = Blueprint('patologys', __name__)



@patologys.route('/patologias/patologias_index')
def patologia_index():

    return patology.index() 

patologys.add_url_rule("/patologias/patologia_save", "patologia_save", patology.save, methods=["POST"])