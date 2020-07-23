from flask import Blueprint , request , render_template , jsonify
from flask_jwt_extended import jwt_required, create_access_token, decode_token
from ..extensiosn import db 
from ..models import User
import bcrypt


@post_api.route('/users/<int:id>/posts/', methods=['POST'])
def create(id):

    data = request.json

   
    postdescription = data.get('postdescription')

    if not postdescription  :
        return {'error': 'dados insuficientes'}, 400

    owner = User.query.get_or_404(id)

    post = Posts(  postdescription=postdescription, owner_id=owner.id)

    db.session.add(post)
    db.session.commit()

    return post.json(), 201


    import cloudinary.uploader

    image_url=db.Column(db.String(300))


#NÃO ESTÁ TERMINADO 
# PARTE DE ADICIONAR IMAGENS E VIDEOS   
'''@imagem.route('/user/<int:id>/img', methods='POST')

    def image_upload(id):
        file = request.files['nome que vamos botar no insomnia']
        
        if not file:
            return {'error': 'Nenhum arquivo'}

         #for('app')
        cloudinary.uploader.upload(file= file , folder=' botar aqui pasta do cloudinary', resource_type='image' , public_id='nome que vc vai dar pra imagem')

        return {} , 204

#NÃO ESTÁ TERMINADO
@imagem.route('/users/file/<int:id>' , methods='POST')

        user = User.query.get_or_404(id)

        #userimg_url = request.json.get('url')

        db.session.add(user)
        db.session.commit()

        return {} , 204'''