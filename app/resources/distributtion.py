from flask import redirect, render_template, request, url_for, abort, session, flash
from sqlalchemy.sql.expression import true
from app.helpers.auth import authenticated
from app.helpers.verifications import user_has_permission
from app.models.user import User
from app.models.vaccine import Vaccine
from app.models.distributtion import Distributtion
from app.models.rol import Rol
import re


def index():
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "vaccine_index"):  
        abort(401)

    vaccines = Vaccine.get_all_vaccines()
    distributtiones = Distributtion.get_all_distributtiones()

    return render_template(
        "distribuciones/distributtion_index.html",
        vaccines=vaccines,
        distributtiones= distributtiones,
    )


def new():
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "vaccine_new"):  #agregar permisos
        abort(401)

    vaccines = User.get_all_users()
    distributtiones = Distributtion.get_all_distributtiones()   

    return render_template(
        "distribuciones/distributtion_index.html",  #cambiar a _new
        distributtion=None,
        message="Realizar Nueva Distribucion",
        mode="create",
        vaccines=vaccines,
        distributtiones= distributtiones,

    )


def save():
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "vaccine_new"):  #cambiar perrmiso 
        abort(401)

    new_distributtion = request.form.copy()
    new_distributtion.pop("id", None)

    Distributtion(**new_distributtion).save()
    flash("Éxito en la operación")
    return redirect(url_for("distributtiones.distributtion_index"))


