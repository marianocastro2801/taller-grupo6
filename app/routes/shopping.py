from app.models import shopping
from flask import Blueprint, request, session, render_template
from app.resources import shopping
from app.models.shopping import Shopping

shoppings = Blueprint('shoppings', __name__)
  

@shoppings.route('/compras/shopping_index') 
@shoppings.route('/compras/shopping_index') 
def shopping_index():
    
    enfermedad_id = request.args.get('enfermedad_id', '2')

    return shopping.index(enfermedad_id)


shoppings.add_url_rule("/compras/shopping_new", "shopping_new", shopping.new)
shoppings.add_url_rule("/compras/shopping_save", "shopping_save", shopping.save, methods=["POST"])
shoppings.add_url_rule("/compras/shopping_update", "shopping_update", shopping.update, methods=["POST"])


@shoppings.route('/compras/<int:shopping_id>')
def shopping_edit(shopping_id):
    return shopping.edit(shopping_id)

