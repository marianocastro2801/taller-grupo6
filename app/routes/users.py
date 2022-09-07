from email.policy import default
from flask import Blueprint, request
from app.resources import user

users = Blueprint('users', __name__)


users.add_url_rule("/usuarios/user_new", "user_new", user.new)
users.add_url_rule("/usuarios/user_save", "user_save", user.save, methods=["POST"])
users.add_url_rule("/usuarios/user_edit/<int:user_id>", "user_edit", user.edit)
users.add_url_rule("/usuarios/user_delete/<int:user_id>", "user_delete", user.delete)
users.add_url_rule("/usuarios/user/<int:user_id>", "user_profile", user.profile)


@users.route('/Usuarios/user_index')
@users.route('/Usuarios/user_index')
def user_index():
    
    return user.index()


