from flask import request, Blueprint, jsonify
from ..models import User
from ..extensions import db

interactions_api = Blueprint('interactions', __name__)

@interactions_api.route('/users/<int:id>/interactions/', methods=['POST'])
def create(id):

    data = request.json

    
    comments = data.get('comments')
    liked = data.get('Liked')

    owner_users = User.query.get_or_404(id)
    owner_photos = photos.query.get_or_404()

    interactions = Interaction(comments = comments , liked=liked , owner_user = owner_users.id, owner_photos )


    
    return product.json(), 201

