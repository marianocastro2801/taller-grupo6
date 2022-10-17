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
from app.models.vacunattion import Vacunattion
from app.models.distributtion import Distributtion
from app.models.patient import Patient
from app.models.rol import Rol
import re


def index(enfermedad_id):
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "vacunattion_index"):  
        abort(401)

    distributtiones = Distributtion.get_filtered(enfermedad_id) #de una enferemdad_id
    enfermedades = VaccineEnfermedad.get_all_enfermedades()
    tot = sumar_cantidades(distributtiones)
    vacunattiones = Vacunattion.get_all_vacunaciones()
    vacuna = VaccineEnfermedad.get_by_id(enfermedad_id)
    vacuna = vacuna.nombre

    return render_template(
        "vacunaciones/vacunattion_index.html",
        vacunattiones= vacunattiones,
        tot = tot,
        distributtiones = distributtiones,
        enfermedades= enfermedades,
        vacuna= vacuna,
    )


def sumar_cantidades (distributtiones):
    suma = 0
    
    for numero in distributtiones:
            suma+= numero.cantidad
    return suma


def new():
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "vacunattion_new"):  
        abort(401)

    pacientes = Patient.get_all_pacientes()
    enfermedades = VaccineEnfermedad.get_all_enfermedades()

    return render_template(
        "vacunaciones/vacunattion_new.html",
        vacunattion=None,
        message="Registrar Vacunacion",
        mode="create",
        pacientes=pacientes,
        enfermedades = enfermedades,

    )

def save():
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "vacunattion_new"): 
        abort(401)

    new_vacunattion = request.form.copy()
    new_vacunattion.pop("id", None)

    Vacunattion(**new_vacunattion).save()
    flash("Éxito en la operación")
    return redirect(url_for("vacunattiones.vacunattion_index"))
