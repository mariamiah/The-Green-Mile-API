from flask import request, jsonify, Blueprint
from api.models.user_models import User

user = Blueprint('user', __name__)
user_obj = User()

@user.route('/api/v1/auth/signup', methods=['POST'])
def register_user():
    """
    Registers a User
    """
    data = request.get_json()
    user_obj.create_user(data)
    return jsonify({"message": "user successfully created"}), 201