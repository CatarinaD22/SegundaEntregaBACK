from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from ..models import User
from ..extensions import db
import bcrypt

auth_api = Blueprint('auth_api', __name__)

#FAZENDO O LOGIN

@auth_api.route('/login', methods=['POST'])
def login():

    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not data or not email or not password:
        return {'error': 'dados insuficientes'}, 400

    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.checkpw(password.encode(), user.password_hash):
        return {'error': 'dados invalidos'}, 400

    token = create_access_token(identity=user.id)

    return {'token': token}, 200