from flask import redirect, render_template, request, url_for, abort, session, flash
from app.models.user import User


def login():
    return render_template("auth/login.html")


def authenticate():
    user = User.get_user_by_email_and_password(**request.form)

    if not user:
        flash("Usuario o clave incorrecto.")
        return redirect(url_for("auth.login"))

    if not user.is_valid():
        flash("Usuario invalido")
        return redirect(url_for("auth.login"))

    session["user"] = {
        "information" : user.get_relevant_data(), 
        "permissions": user.get_permissions()
        }
        
    return redirect(url_for("home.view"))


def logout():
    del session["user"]
    session.clear()

    return redirect(url_for("auth.login"))
