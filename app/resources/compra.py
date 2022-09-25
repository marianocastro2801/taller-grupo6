from flask import redirect, render_template, request, url_for, abort, session, flash
from sqlalchemy.sql.expression import true
from app.helpers.auth import authenticated
from app.helpers.verifications import user_has_permission
from app.models.user import User
from app.models.shopping import Shopping
from app.models.vaccine import Vaccine
from app.models.vaccine_lote import VaccineLote
from app.models.vaccine_developer import VaccineDeveloper
from app.models.rol import Rol
import re
import datetime



def index():
    if not authenticated(session):
        return redirect(url_for("auth.login"))


    shoppings = Shopping.get_all_shoppings()
    return render_template(
        "compras/buy_index.html",
        shoppings=shoppings,
    )

#def index(vacuna_id):
#    if not authenticated(session):
#        return redirect(url_for("auth.login"))
#    if not user_has_permission(session, "vaccine_index"):
#        abort(401)

#    compras = Shopping.get_shoppings_by_vaccine(vacuna_id)
#    return render_template(
#        "compras/buy_index.html",
#        compras=compras,
#        vacuna_id=vacuna_id,
#    )

def new():
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "vaccine_index"):  #deberia ser: shopping_create : agregar permisos
        abort(401)

    shoppings = Shopping.get_all_shoppings()
    vaccines = Vaccine.get_all_vaccines()
    lotes = VaccineLote.get_all_lotes()
    developers = VaccineDeveloper.get_all_desarrolladores()

    return render_template(
        "compras/buy_new.html",
        shopping=None,
        message="Registrar Nueva Compra",
        mode="create",
        shoppings = shoppings,
        vaccines=vaccines,
        lotes = lotes,
        developers = developers,


    )

def save():
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "vaccine_index"):  #seria: vaccine_create : agregar permisos
        abort(401)

    new_shopping = request.form.copy()
    new_shopping.pop("id", None)

    Shopping(**new_shopping).save()
    flash("Éxito en la operación")
    return redirect(url_for("shoppings.buy_index"))


def edit(shopping_id):
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "vaccine_index"): #seria: shopping_.... : agregar permisos. POOR AHORA SOLO INDEX
        abort(401)

    shopping = Shopping.get_by_id(shopping_id)
# necesitaria los estados de la compra de otra tabla   

    return render_template("compras/shopping_new.html",
        message="Editar compra", mode="edit"

    )
    

def update():
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "vaccine_index"): #seria: shopping_.... : agregar permisos. POOR AHORA SOLO INDEX
        abort(401)

    new_shopping = request.form.copy()

    Shopping.update(**new_shopping)

    flash("Éxito en la operación")
    return redirect(url_for("shoppings.buy_index"))