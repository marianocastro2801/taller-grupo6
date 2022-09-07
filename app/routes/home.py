from flask import Blueprint, request, render_template, session, redirect, url_for
from app.helpers.auth import authenticated

home = Blueprint('home', __name__)


def home_view():
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    return render_template("home.html")


home.add_url_rule("/", "view", home_view)
