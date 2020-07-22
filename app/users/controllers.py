from flask import Blueprint , request , render_template , jsonify
from flask_jwt_extended import jwt_required, create_access_token, decode_token
from ..extensiosn import db 
from ..models import User
import bcrypt

user_api = Blueprint ('user_api', __name__)


#CRIANDO UM USUÁRIO NOVO
@user_api.route('/users/', methods=['POST'])
def create():
    
    #Pegando os dados do body
    data = request.json
    # Pego parte a parte os argumentos do body
    name = data.get("name")
    email = data.get("email")
    password = data.get('password')

    
    #Checando se não falta algum dado essencial como nome e email
    if not name or not email or not password:
        return {'erro': 'Dados insuficientes'}, 400


    user_check = User.query.filter_by(email=email).first()

    if user_check:
        return {'error': 'Email já cadastrado'}, 400
    #Checando a existência de algum user no bd com o mesmo email, se houver 1 user já com o email, impedir o cadastro e mostrar o erro
    
    password_hash = bcrypt.hashpw(password.encode() , bcrypt.gensalt())
       
       
    user = User(name = name, email = email ,  password_hash=password_hash)

    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity= user.id)
             
    
    return user.json() ,200




