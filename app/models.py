from .extensions import db


class User(db.Model):
    __tabelname__= 'users'
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(20), unique = True , nullable= False)
    

    password_hash=db.Column(db.String(128), nullable=False)
    active =db.Column(db.Boolean, default=False)

    def json(self):
        user_json = { 'id': self.id,
                    'name': self.name,
                    'email': self.email
                   
                    

        }
        return user_json

 class Product(db.Model):

    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    price= db.Column(db.Integer , nullable = False)
    description = db.Column(db.String(200), nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def json(self):

        return {'name': self.name,
                'price' : self.price,
                'desciption': self.description,
                'id': self.id,
                'owner': self.owner.json()}       
