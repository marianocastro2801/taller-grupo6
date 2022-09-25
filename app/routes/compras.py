from app.models import shopping
from flask import Blueprint, request, session, render_template
from app.resources import compra
from app.models.shopping import Shopping

shoppings = Blueprint('shoppings', __name__)
  
@shoppings.route('/compras/buy_index')
@shoppings.route('/compras/buy_index')
def shopping_index():
    
    return compra.index() 


shoppings.add_url_rule("/compras/shopping_new", "shopping_new", compra.new)
shoppings.add_url_rule("/compras/shopping_save", "shopping_save", compra.save, methods=["POST"])
shoppings.add_url_rule("/compras/shopping_update", "shopping_update", compra.update, methods=["POST"])

@shoppings.route('/compras/editar/<int:shopping_id>')
def shopping_edit(shopping_id):
    return shopping.edit(shopping_id)