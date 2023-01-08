from queue import Empty
from app.models.vaccine_enfermedad import VaccineEnfermedad
from flask import redirect, render_template, request, url_for, abort, session, flash
from sqlalchemy.sql.expression import true
from app.helpers.auth import authenticated
from app.helpers.verifications import user_has_permission
from app.models.user import User
from app.models.vaccine import Vaccine
from app.models.distributtion import Distributtion
from app.models.shopping import Shopping
from app.models.provincias import Province
from app.models.vaccine_lote import VaccineLote
from app.models.vaccine_vencidas import VaccineVencida
from app.models.rol import Rol
import re


def index():
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "distributtion_index"):  
        abort(401)

    vaccines = Vaccine.get_all_vaccines()
    distributtiones = Distributtion.get_all_distributtiones()
    lotes = VaccineLote.get_all_lotes()

    return render_template(
        "distribuciones/distributtion_index.html",
        vaccines=vaccines,
        distributtiones= distributtiones,
        lotes = lotes,
    )


def new():
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "distributtion_new"):  
        abort(401)

    enfermedades = VaccineEnfermedad.get_all_enfermedades()
   #shoppings = Shopping.get_filtered(enfermedad_id)
    distributtiones = Distributtion.get_all_distributtiones()
    provincias = Province.get_all_provincias()
    lotes = VaccineLote.get_all_lotes()   

    return render_template(
        "distribuciones/distributtion_new.html",  
        distributtion=None,
        message="Realizar Nueva Distribucion",
        mode="create",
        enfermedades= enfermedades,
        distributtiones= distributtiones,
        provincias = provincias,
        lotes = lotes,

    )


def save():
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "distributtion_new"):   
        abort(401)

    new_distributtion = request.form.copy()
    new_distributtion.pop("id", None) 

#antes de distribuir debo ver si alcanza el stock nacional
    d = new_distributtion.pop("enfermedad_id")
    c = new_distributtion.pop("cantidad")
    shoppings = Shopping.get_filtered(d)
    tot = sumar_cantidades(shoppings) 
#tot es el stock y c cantidad a distribuir
   

    if tot < int(c) :
    
        flash("No hay Stock disponible para la distribucion en estos momentos.")
        return redirect(url_for("distributtiones.distributtion_index"))
    
    
#AQUI HAY QUE GUARDAR LAS VENCIDAS EN SU TABLA
#    distributtiones = Distributtion.get_filtered(d)
#    p = new_distributtion.pop("provincia_id")
#    distributtiones = Distributtion.get_filtered_provincia(p)
#    sum = 0
#    for d in distributtiones:
#        if d.lote_id == 5:
#            sum+= d.cantidad
#        VaccineVencida.cantidad = sum 

#    VaccineVencida.enfermedad = "una enfermedad" 
#    VaccineVencida.provincia = "una provincia" 
    
   
    
    
    
    
    new_distributtion = request.form.copy()
    new_distributtion.pop("id", None) 
    Distributtion(**new_distributtion).save()
    flash("Distribucion Registrada Exitosamente")
    return redirect(url_for("distributtiones.distributtion_index"))


def sumar_cantidades (shoppings):
    suma = 0
    
    #solo voy a contabilizar aquellas compras que tengan estado = Entregado
    for numero in shoppings:
        if (numero.estado_id == 3):
            suma+= numero.cantidad_vacunas
    return suma 


