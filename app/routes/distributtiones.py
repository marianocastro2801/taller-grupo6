from flask import Blueprint, request, session, render_template
from app.resources import distributtion

distributtiones = Blueprint('distributtiones', __name__)
  

@distributtiones.route('/distribuciones/distributtion_index') 
@distributtiones.route('/distribuciones/distributtion_index') 
def distributtion_index():
    

    return distributtion.index()


distributtiones.add_url_rule("/distribuciones/distributtion_new", "distributtion_new", distributtion.new)
distributtiones.add_url_rule("/distribuciones/distributtion_save", "distributtion_save", distributtion.save, methods=["POST"])

