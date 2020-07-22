from flask import request, Blueprint, jsonify
from ..models import User, Product
from flask_jwt_extended import jwt_required
from ..extensions import db

product_api = Blueprint('product_api', __name__)

#ANUNCIANDO UM PRODUTO 
@product_api.route('/users/<int:id>/products/', methods=['POST'])
def create(id):

    data = request.json

    name = data.get('name')
    price = data.get('price')
    description = data.get('description')

    if not data or not name or not description or not price:
        return {'error': 'dados insuficientes'}, 400

    owner = User.query.get_or_404(id)

    product = Product(name=name,price=price, description=description, owner_id=owner.id)

    db.session.add(product)
    db.session.commit()

    return product.json(), 201

    