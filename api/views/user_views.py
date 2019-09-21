from flask import request, jsonify, Blueprint
from api.controllers.user_controller import UserController
from flask_jwt_extended import jwt_required

user = Blueprint('user', __name__)
user_controller = UserController()


@user.route('/api/v1/auth/signup', methods=['POST'])
@jwt_required
def register_user():
    """
    Registers a User
    """
    data = request.get_json()
    token = request.headers['Authorization']
    fetched_token = token.split(" ")[1]
    if user_controller.check_user_permission(fetched_token):
        return user_controller.register_user_controller(data)
    return jsonify({"message": "No permissions to add a user"}), 401
    
@user.route('/api/v1/auth/login', methods=['POST'])
def login():
    """
    Logs in User
    """
    data = request.get_json()
    return user_controller.login_controller(data)
