from xmlrpc.client import boolean
from app.models import vaccine
from app.models import vaccine_lote
from app.models import shopping
from app.models.vaccine_type import VaccineType
from flask import redirect, render_template, request, url_for, abort, session, flash
from sqlalchemy.sql.expression import true
from app.helpers.auth import authenticated
from app.helpers.verifications import user_has_permission
from app.models.user import User
from app.models.shopping import Shopping
from app.models.vaccine import Vaccine
from app.models.vaccine_lote import VaccineLote
from app.models.vaccine_developer import VaccineDeveloper
from app.models.vaccine_enfermedad import VaccineEnfermedad
from app.models.rol import Rol
import re
import datetime





def index(enfermedad_id):
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "vaccine_index"):
        abort(401)
 
    vacuna = VaccineEnfermedad.get_by_id(enfermedad_id)
    vacuna = vacuna.nombre
    shoppings = Shopping.get_filtered(enfermedad_id)

    tot = sumar_cantidades(shoppings)   
    vaccines = Vaccine.get_all_vaccines()
    lotes = VaccineLote.get_all_lotes()
    developers = VaccineDeveloper.get_all_desarrolladores()
    enfermedades = VaccineEnfermedad.get_all_enfermedades()


    return render_template(
        "compras/shopping_index.html",
        shoppings=shoppings,
        vaccines = vaccines,
        lotes = lotes,
        developers=developers,
        tot = tot,
        enfermedades = enfermedades,
        vacuna = vacuna,
   
    ) 

def sumar_cantidades (shoppings):
    suma = 0
    
    #solo voy a contabilizar aquellas compras que tengan estado = Entregado
    for numero in shoppings:
        if (numero.estado_id == 3):
            suma+= numero.cantidad_vacunas
    return suma

def new():
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "vaccine_index"):  
        abort(401)

    shoppings = Shopping.get_all_shoppings()
    vaccines = Vaccine.get_all_vaccines()
    lotes = VaccineLote.get_all_lotes()
    developers = VaccineDeveloper.get_all_desarrolladores()
    enfermedades = VaccineEnfermedad.get_all_enfermedades()

    return render_template(
        "compras/shopping_new.html",
        shopping= None,
        shoppings=shoppings,
        message="Registrar Nueva Compra",
        mode="create",
        vaccines=vaccines,
        lotes = lotes,
        developers= developers,
        enfermedades=enfermedades,
    )

def save():
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "shopping_new"):  
        abort(401)

    new_shopping = request.form.copy()
    new_shopping.pop("id", None)

    Shopping(**new_shopping).save()
    flash("Se ha registrado la compra exitosamente")
    return redirect(url_for("shoppings.shopping_index"))


    

def update():
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "vaccine_index"): #seria: shopping_.... : agregar permisos. POOR AHORA SOLO INDEX
        abort(401)

    new_shopping = request.form.copy()

    Shopping.update(**new_shopping)

    flash("Éxito en la operación")
    return redirect(url_for("shoppings.shopping_index"))


def toggle_activation():
    if not authenticated(session):
        return redirect(url_for("auth.login"))

    if not user_has_permission(session,"shopping_index"): #permiso para cambiar estado
        abort(401)
        
    id = request.form["shopping_id"]
    shopping = Shopping.get_by_id(id)

    if (shopping.estado_id == 1):   #pagar funciona
       shopping.pagar()

    else:
       shopping.entregar()      #entregar funciona
    
    flash("Éxito en la operación")
   
    #return redirect(url_for("shoppings.shopping_index"))
    return index([shopping.enfermedad_id])
    # intenetar que se redireccione a la misma enfermedad
    # FUNCIONAAAA! :=)