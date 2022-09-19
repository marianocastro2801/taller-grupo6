from flask import redirect, render_template, request, url_for, abort, session, flash
from sqlalchemy.sql.expression import true
from app.helpers.auth import authenticated
from app.helpers.verifications import user_has_permission
from app.models.user import User
from app.models.vaccine import Vaccine
from app.models.vaccine_type import VaccineType
from app.models.rol import Rol
import re


def index():
    if not authenticated(session):
        return redirect(url_for("auth.login"))


    vaccines = Vaccine.get_all_vaccines()
    return render_template(
        "Vacunas/vaccine_index.html",
        vaccines=vaccines,
    )


def new():
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "vaccine_index"):  #seria: vaccine_create : agregar permisos
        abort(401)

    vaccines = User.get_all_users()
    types = VaccineType.get_all_types()
  
    return render_template(
        "vacunas/vaccine_new.html",
        vaccine=None,
        message="Registrar nueva vacuna",
        mode="create",
        vaccines=vaccines,
        types=types,

    )


def save():
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "vaccine_index"):  #seria: vaccine_create : agregar permisos
        abort(401)

    new_vaccine = request.form.copy()
    new_vaccine.pop("id", None)

    Vaccine(**new_vaccine).save()
    flash("Éxito en la operación")
    return redirect(url_for("vaccines.vaccine_index"))


def edit(vaccine_id):
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "vaccine_index"): #seria: vaccine_update : agregar permisos. POOR AHORA SOLO INDEX
        abort(401)

    vaccine = Vaccine.get_by_id(vaccine_id)
    types = VaccineType.get_all_types()

    return render_template("vacunas/vaccine_new.html", vaccine=vaccine,
        message="Editar vacuna", mode="edit", types=types

    )
    

def update():
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "vaccine_index"): #seria: vaccine_update : agregar permisos. POOR AHORA SOLO INDEX
        abort(401)

    new_vaccine = request.form.copy()

    #Vaccine.update(**request.form)
    Vaccine.update(**new_vaccine)

    flash("Éxito en la operación")
    return redirect(url_for("vaccines.vaccine_index"))
    

def delete(vaccine_id):
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "vaccine_index"):
        abort(401)

    Vaccine.delete(vaccine_id)
    flash("Éxito en la operación")
    return redirect(url_for("vaccines.vaccine_index"))