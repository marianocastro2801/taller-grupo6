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


def index(search, type_id):
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "vaccine_index"):  
        abort(401)

    vaccines = Vaccine.get_filtered(search,type_id)
    lotes = VaccineLote.get_all_lotes()
    developers = VaccineDeveloper.get_all_desarrolladores()

    return render_template(
        "Vacunas/vaccine_index.html",
        vaccines=vaccines,
        lotes= lotes,
        developers=developers,
    )


def new():
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "vaccine_new"):  
        abort(401)

    vaccines = User.get_all_users()
    lotes = VaccineLote.get_all_lotes()
    types = VaccineType.get_all_types()
    developers = VaccineDeveloper.get_all_desarrolladores()
    enfermedades = VaccineEnfermedad.get_all_enfermedades()

    return render_template(
        "vacunas/vaccine_new.html",
        vaccine=None,
        message="Registrar Vacuna Nueva",
        mode="create",
        vaccines=vaccines,
        types=types,
        developers = developers,
        lotes= lotes,
        enfermedades = enfermedades,

    )


def save():
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "vaccine_new"): 
        abort(401)

    new_vaccine = request.form.copy()
    new_vaccine.pop("id", None)

    Vaccine(**new_vaccine).save()
    flash("Éxito en la operación")
    return redirect(url_for("vaccines.vaccine_index"))


def edit(vaccine_id):
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "vaccine_update"):
        abort(401)
#no debo editar o eliminar una vacuna si ya tiene compras
    vaccine = Vaccine.get_by_id(vaccine_id)
    types = VaccineType.get_all_types()
    developers = VaccineDeveloper.get_all_desarrolladores()
    enfermedades = VaccineEnfermedad.get_all_enfermedades()

    shoppings = Shopping.get_shoppings_by_vaccine(vaccine_id)
    if is_list_empty(shoppings):

        return render_template("vacunas/vaccine_new.html", vaccine=vaccine,
        message="Editar vacuna", mode="edit", types=types, developers= developers, enfermedades=enfermedades)
    else: 

        flash("No puede editar una vacuna que posea compras")
        return redirect(url_for("vaccines.vaccine_index"))
    
    

def update():
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "vaccine_update"):
        abort(401)

    new_vaccine = request.form.copy()


    Vaccine.update(**new_vaccine)

    flash("Éxito en la operación")
    return redirect(url_for("vaccines.vaccine_index"))
    

def delete(vaccine_id):
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "vaccine_delete"):
        abort(401)
    #no se puede eliminar una vacuna con compras realizadas
    shoppings = Shopping.get_shoppings_by_vaccine(vaccine_id)
    
    if is_list_empty(shoppings):
        Vaccine.delete(vaccine_id)
        flash("Éxito en la operación")
        return redirect(url_for("vaccines.vaccine_index")) 
    else: 
        flash("No puede eliminar una vacuna que posea compras")
        return redirect(url_for("vaccines.vaccine_index"))
    
    # function to check whether the list is empty or not
def is_list_empty(shoppings):
    # checking the length
    if len(shoppings) == 0:
        # returning true as length is 0
        return True
    # returning false as length is greater than 0
    return False