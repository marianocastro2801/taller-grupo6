from app.models.shopping import Shopping
from flask import redirect, render_template, request, url_for, abort, session, flash
from sqlalchemy.sql.expression import true
from app.helpers.auth import authenticated
from app.helpers.verifications import user_has_permission
from app.models.user import User
from app.models.vaccine import Vaccine
from app.models.vaccine_type import VaccineType
from app.models.vaccine_lote import VaccineLote
from app.models.vaccine_developer import VaccineDeveloper
from app.models.vaccine_enfermedad import VaccineEnfermedad
from app.models.rol import Rol
import re


def index():
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "patology_index"):  
        abort(401)

    patologys = VaccineEnfermedad.get_all_enfermedades()
   

    return render_template(
        "patologias/patologias_index.html",
        patologys=patologys,   
    )

def save():
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "patology_index"):
        abort(401)

    v= VaccineEnfermedad(**request.form)
    v.save()
    
  
    flash("Exito en la operacion")
    return index() 
    
