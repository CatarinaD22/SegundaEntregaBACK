from flask import Flask , request , jsonify , render_template
from flask_sqlalchemy import SQLAlchemy

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import bcrypt
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data-dev.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS']= False

'''app.config['MAIL_SEVER']= 
app.config['MAIL_PORT']=
app.config['MAIL_USERNAME']=
app.config['MAIL_PASSWORD']=
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL']= False'''

app.config['JWT_SECRET_KEY'] = 'senha'  
jwt = JWTManager(app)


db = SQLAlchemy(app)


class User(db.Model):
    __tabelname__= 'users'
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(20), unique = True , nullable= False)
    idade = db.Column(db.Integer , default=0)

    password_hash=db.Column(db.String(128), nullable=False)
    active =db.Column(db.Boolean, default=False)

    def json(self):
        user_json = { 'id': self.id,
                    'name': self.name,
                    'email': self.email,
                    'idade': self.idade
                    

        }
        return user_json


@app.route('/users/', methods=['POST'])
def create():
    
    #Pegando os dados do body
    data = request.json
    # Pego parte a parte os argumentos do body
    name = data.get("name")
    email = data.get("email")
    idade = data.get("idade")
    password= data.get('password')

    
    #Checando se não falta algum dado essencial como nome e email
    if not name or not email or not password:
        return {'erro': 'Dados insuficientes'}, 400


    user_check = User.query.filter_by(email=email).first()

    if user_check:
        return {'error': 'Usuário já cadastrado'}, 400
    #Checando a existência de algum user no bd com o mesmo email, se houver 1 user já com o email, impedir o cadastro e mostrar o erro
    
    password_hash = bcrypt.hashpw(password.encode() , bcrypt.gensalt())
       
       
    user = User(name = name, email = email , idade=idade , password_hash=password_hash)
    db.session.add(user)
    db.session.commit()

    '''msg=Message(sender='',
                recipients=[email],
                subject='Bem Vindo!',
                html=render_template('' , name=name))

    mail.send(msg)    '''        
    
    return user.json() ,200

@app.route('/users/', methods=['GET'] )
def index(): #mostra todos os usuários
   
    users = User.query.all()

    return jsonify([user.json() for user in users]) , 200

@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email:
        return jsonify({"msg": "Falta o email"}), 400
    if not password:
        return jsonify({"msg": "Falta a senha"}), 400


    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200

   
@app.route('/users/<int:id>' , methods=["GET", "PUT" , "PATCH" , "DELETE" , ])
@jwt_required

def user_detail(id):
    #Checar se a pessoa fez o login para poder ou não deixar ela fazer as ações
    user = User.query.get_or_404(id)
    current_user = get_jwt_identity()
    if user.email != current_user:
        return {'error' : 'Acesso não permitido'} , 400
   
    if request.method == 'GET':
        user = User.query.get_or_404(id)
        return user.json(), 200
   
    #Testo para checar se a requisição é um PUT
    elif request.method == 'PUT' :
        
        # Pego os dados do body
        data = request.json

        if not data :
            return {'error': 'Requisição precisa de body'} , 400
        # Pego parte a parte os argumentos do body
        novoname = data.get("name")
        novoemail = data.get("email")
        novaidade = data.get("idade")

        #Checar se os dados necessários foram enviados
        if not novoname or not novoemail:
            return   'Erro: Dados insuficientes', 400

        
        #Recebo o user com a id da requisição
        user = User.query.get_or_404(id)
        
        #Altero todas as partes do User com os novos dados
        user.name = novoname
        user.email = novoemail
        user.idade = novaidade
        
        #Adiciono esse novo user (no id original)
        db.session.add(user)
        db.session.commit()
        
        #Retorno o user e o status de que tudo ocorreu devidamente
        return user.json(), 200

    #Testo para checar se a requisição é um PATCH
    elif request.method == 'PATCH':
        data = request.json

        if not data:
            return {'error': 'Requisição precisa de body'}, 400

        email = data.get('email')

        if User.query.filter_by(email=email).first() and email != user.email:
            return {'error': 'Email já cadastrado'}, 400

        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.idade = data.get('idade', user.idade)

        #Adiciono esse novo user que apenas te o email alterado no mesmo id original
        db.session.add(user)
        db.session.commit()

        #Retorno o user e o status de que tudo ocorreu devidamente
        return user.json(), 200
        



    #Testo para checar se a requisição é um DELETE    
    elif request.method == 'DELETE':

        #Recebo o user do id requisitado
        user = User.query.get_or_404(id)

        #Apago o user do id requisitado
        db.session.delete(user)
        db.session.commit()

        ##Retorno o user e o aviso de que o usuário foi deletado com sucesso e um status de que tudo ocorreu devidamente
        return "Usuário deletado com sucesso." , 200




if __name__ == '__main__':
    app.run(debug=True)