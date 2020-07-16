from flask import Flask , request , jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data-dev.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JSON_SORT_KEYS']= False
db = SQLAlchemy(app)

class User(db.Model):
    __tabelname__= 'users'
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(20), unique = True , nullable= False)
    idade = db.Column(db.Integer , default=0)

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

    #Checando se não falta algum dado essencial como nome e email
    if not name or not email:
        return {'erro': 'Dados insuficientes'}, 400

    #Checando a existência de algum user no bd com o mesmo email, se houver 1 user já com o email, impedir o cadastro e mostrar o erro
    if  db.session.query(User).filter_by(email=email).count() < 1:
        user = User(name = name, email = email , idade=idade)
        db.session.add(user)
        db.session.commit()
    
    else:
        return  "Email já em uso" , 400

    return user.json() ,200

@app.route('/users/', methods=['GET'] )
def index(): #mostra todos os usuários
   
    users = User.query.all()

    return jsonify([user.json() for user in users]) , 200


@app.route('/users/<int:id>' , methods=["GET", "PUT" , "PATCH" , "DELETE" , "POST"])

def user_detail(id):
    if request.method == 'GET':
        user = User.query.get_or_404(id)
        return user.json(), 200
   
    #Testo para checar se a requisição é um PUT
    elif request.method == 'PUT' :
        
        # Pego os dados do body
        data = request.json
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

        #Pego o dado do novo email
        novoemail= data.get("email")

        #Recebo o email antigo
        user = User.query.get_or_404(id)

        #Coloco o email novo no lugar do antigo
        user.email= novoemail

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