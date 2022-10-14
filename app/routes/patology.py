from asyncio.windows_events import NULL
from contextlib import nullcontext
from email.policy import default
from flask import Blueprint, request
from app.resources import patology


patologys = Blueprint('patologys', __name__)



@patologys.route('/patologias/patologias_index')
def patologia_index():

    return patology.index() 

patologys.add_url_rule("/patologias/patologia_save", "patologia_save", patology.save, methods=["POST"])