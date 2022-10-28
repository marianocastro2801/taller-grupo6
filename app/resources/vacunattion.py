from app.models.provincias import Province
from app.models.shopping import Shopping
from flask import redirect, render_template, request, url_for, abort, session, flash
from datetime import date, time, datetime
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

    #vacunattiones = Vacunattion.get_vacunattiones_by_provincia(provincia_id)
    distributtiones = Distributtion.get_filtered(enfermedad_id) #de una enferemdad_id
    enfermedades = VaccineEnfermedad.get_all_enfermedades()
    tot = sumar_cantidades(distributtiones)
    #vacunattiones = Vacunattion.get_all_vacunaciones()
    vacunattiones = Vacunattion.get_vacunattiones_by_enfermedad(enfermedad_id)
    vacuna = VaccineEnfermedad.get_by_id(enfermedad_id)
    vacuna = vacuna.nombre
    provincias = Province.get_all_provincias()

    return render_template(
        "vacunaciones/vacunattion_index.html",
        vacunattiones= vacunattiones,
        tot = tot,
        distributtiones = distributtiones,
        enfermedades= enfermedades,
        vacuna= vacuna,
        provincias= provincias,
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
    provincias = Province.get_all_provincias()

    return render_template(
        "vacunaciones/vacunattion_new.html",
        vacunattion=None,
        message="Registrar Vacunacion",
        mode="create",
        pacientes=pacientes,
        enfermedades = enfermedades,
        provincias= provincias,

    )

def save():
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "vacunattion_new"): 
        abort(401)

    new_vacunattion = request.form.copy()
    new_vacunattion.pop("id", None)

#validar las vacunaciones antes de guardar
    e = new_vacunattion.pop("enfermedad_id")
    f = new_vacunattion.pop("fecha_vacunacion")

    fecha1 = date(2010, 1, 1)
    fecha2 = date(2010, 12, 31)
    
#IMPEDIR VACUNACION SI NO HAY STOCK 
    if e == "19": #pandemia 2010
        if format(f) < str(fecha1) or format(f) > str(fecha2):
            flash("La vacunacion de la pandemia 2010 ya finalizo, corresponde al año 2010") 
            return redirect(url_for("vacunattiones.vacunattion_index"))
        else:
            new_vacunattion = request.form.copy()
            new_vacunattion.pop("id", None) 
            Vacunattion(**new_vacunattion).save()
            flash("La vacunacion se registro exitosamente") 
            return redirect(url_for("vacunattiones.vacunattion_index"))
#-------------------------------------------------------------------------------
    fecha1 = date(2020, 1, 1)
    fecha2 = date(2023, 12, 31)

    if e == "1": #covid 19
        if format(f) < str(fecha1) or format(f) > str(fecha2):
            flash("La vacunacion de Covid-19 ya finalizo, finalizo la pandemia") 
            return redirect(url_for("vacunattiones.vacunattion_index"))
        else:
            new_vacunattion = request.form.copy()
            new_vacunattion.pop("id", None) 
            Vacunattion(**new_vacunattion).save()
            flash("La vacunacion se registro exitosamente") 
            return redirect(url_for("vacunattiones.vacunattion_index"))
#-------------------------------------------------------------------------------   
    fecha1 = date(2022, 1, 1)
    fecha2 = date(2022, 12, 31)
    
    if e == "2": #Antigripal
        if format(f) < str(fecha1) or format(f) > str(fecha2):
            flash("La vacunacion Antigripal ya finalizo, corresponde al año 2022") 
            return redirect(url_for("vacunattiones.vacunattion_index"))
        else:
            new_vacunattion = request.form.copy()
            new_vacunattion.pop("id", None) 
            Vacunattion(**new_vacunattion).save()
            flash("La vacunacion se registro exitosamente") 
            return redirect(url_for("vacunattiones.vacunattion_index"))


#    Vacunattion(**new_vacunattion).save()
#    flash("Éxito en la operación")
#    return redirect(url_for("vacunattiones.vacunattion_index"))


def profile(vacunattion_id):
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    
    vacunattion = Vacunattion.get_by_id(vacunattion_id)
   
    return render_template("vacunaciones/vacunattion_profile.html", vacunattion = vacunattion)
