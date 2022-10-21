from lib2to3.refactor import get_all_fix_names
from flask import jsonify, Blueprint, request, abort
from marshmallow import ValidationError
import werkzeug
from app.schemas.persona import persona_schema
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.persona import persona_schema

persona_api = Blueprint("personas", __name__, url_prefix="/personas")


@persona_api.get("/")
def index():

    json = 1
    return  json
