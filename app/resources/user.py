from asyncio.windows_events import NULL
from flask import redirect, render_template, request, url_for, abort, session, flash
from sqlalchemy.sql.expression import true
from app.helpers.auth import authenticated
from app.helpers.verifications import user_has_permission
from app.models.user import User
from app.models.rol import Rol
import re


def index(search):
    if not authenticated(session):
        return redirect(url_for("auth.login"))

    if not user_has_permission(session,"user_index"):
        abort(401)

    #users = User.get_all_users()
    users = User.get_filtered(search
    )
    return render_template(
        "Usuarios/user_index.html",
        users=users,
    )


def profile(user_id):
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    
    user = User.get_by_id(user_id)
    if user != None:
        return render_template("Usuarios/user_profile.html", user = user)
    else:
        return redirect(url_for("home"))


def new():
    if not authenticated(session):
        return redirect(url_for("auth.login"))

    if not user_has_permission(session,"user_new"):
        abort(401)

    roles = Rol.get_all_roles()
    return render_template(
        "Usuarios/user_new.html",
        user=None,
        roles=roles,
        message="Registrar Usuario Nuevo",
        mode="create",
    )


# Se invoca por GET para determinar el id del usuario a modificar
def edit(user_id):
    if not authenticated(session):
        return redirect(url_for("auth.login"))

    if not user_has_permission(session,"user_update"):
        abort(401)

    user = User.get_by_id(user_id)
    if user != None:
        roles = Rol.get_all_roles()
        return render_template(
            "Usuarios/user_new.html",
            user=user,
            roles=roles,
            message="Editar Usuario",
            mode="edit",
        )
    else:
        return redirect(url_for("users.user_index"))


# Se invoca por GET para determinar el id del usuario a eliminar
def delete(user_id):
    if not authenticated(session):
        return redirect(url_for("auth.login"))

    if not user_has_permission(session,"user_delete"):
        abort(401)

    user = User.get_by_id(user_id)
    if user != None:
        user.remove()
        flash("Éxito en la operación")
        return redirect(url_for("users.user_index"))
    else:
        flash("Ocurrió un error al realizar la operación")
        return redirect(url_for("users.user_index"))


def save():
    if not authenticated(session):
        return redirect(url_for("auth.login"))

    if not user_has_permission(session,"user_delete"):
        abort(401)

    # user = User(**request.form)
    user = User(
        nombre=request.form["nombre"],
        apellido=request.form["apellido"],
        email=request.form["email"],
        usrname=request.form["usrname"]
    )

    roles = request.form['roles'].split(',')
    if roles[0] == "":
        roles = None

    if request.form['mode'] == "create":
        user.password = request.form["password"]
        return create(user, roles)
    else:
        user.id = request.form["user_id"]
        return update(user, roles)


def create(user, roles):   
    if not validar(user):
        if User.mail_esta_disponible(user.email[0]) and User.usrname_esta_disponible(
            user.usrname[0]
        ):
            user.save(roles)
            flash("Éxito en la operación")
            return redirect(url_for("users.user_index"))
    flash("Ocurrió un error al guardar. Verifique los campos")
    return redirect(url_for("users.user_new"))


def update(user, roles):
    if usuarioExiste(user.id):
        if validarEdicion(user):
            try:
                user.update(roles)
                flash("Éxito en la operación")
                return redirect(url_for("users.user_index"))
            except Exception as e:
                print(e)
                flash("Ocurrió un error al guardar. Intente nuevamente.")
                return redirect(url_for("users.user_edit", user_id=user.id))
    flash("Ocurrió un error al guardar. Verifique los campos")
    return redirect(url_for("users.user_edit", user_id=user.id))


def validar(user):
    if user.nombre[0] == "" or len(user.nombre[0]) > 50 or tieneNumeros(user.nombre[0]):
        return False
    elif (
        user.apellido[0] == ""
        or len(user.apellido[0]) > 50
        or tieneNumeros(user.apellido[0])
    ):
        return False
    elif user.email[0] == "" or len(user.email[0]) > 50 or validarEmail(user.email[0]):
        return False
    elif user.usrname[0] == "" or len(user.usrname[0]) > 50:
        return False
    else:
        return True


def usuarioExiste(id):
    return User.get_by_id(id).id != None


def tieneNumeros(inputString):
    respuesta = re.search(r"\d", inputString)
    ok = bool(respuesta)
    return bool(re.search(r"\d", inputString))


def validarEmail(mail):
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    return not (re.fullmatch(regex, mail))


def passwordsCoinciden(pass1, pass2):
    return pass1 == pass2


def toggle_activation():
    if not authenticated(session):
        return redirect(url_for("auth.login"))

    if not user_has_permission(session,"user_delete"):
        abort(401)
        
    id = request.form["usr_id"]
    user = User.get_by_id(id)
    if Rol(nombre='Administrador') not in user.roles:
        if user.activo:
            user.deactivate()
        else:
            user.activate()
        flash("Éxito en la operación")
    else:
        flash("Un administrador no puede ser bloqueado")
    return redirect(url_for("users.user_index"))
    

def validarCreacion(user):
    if not validar(user):
        return False
    elif not validarPass(user):
        return False
    elif not User.mail_esta_disponible(user.email[0]):
        return False
    elif not User.usrname_esta_disponible(user.usrname[0]):
        return False
    else:
        return True


def validarPass(user):
    if (
        user.password == ""
        or len(user.password) > 50
        or not passwordsCoinciden(user.password, request.form["passwordConfirm"])
    ):
        return False
    else:
        return True


def validarEdicion(user):
    if not validar(user):
        return False
    elif not validarMailEdicion(user.email[0], User.get_by_id(user.id).email):
        return False
    elif not validarUsrnameEdicion(user.usrname[0], User.get_by_id(user.id).usrname):
        return False
    else:
        return True


def validarMailEdicion(original, nuevo):
    if original == nuevo:
        return true
    else:
        return User.mail_esta_disponible(nuevo)


def validarUsrnameEdicion(original, nuevo):
    if original == nuevo:
        return true
    else:
        return User.usrname_esta_disponible(nuevo)
