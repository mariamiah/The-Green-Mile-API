from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required
from api.controllers.user_controller import UserController
from api.controllers.helper_controllers import HelperController


user = Blueprint('user', __name__)
user_controller = UserController()
helper_controller = HelperController()


@user.route('/api/v1/auth/signup', methods=['POST'])
@jwt_required
def register_user():
    """
    Registers a User
    """
    data = request.get_json()
    token = helper_controller.get_token_from_request()
    if user_controller.check_user_permission(token) == 'Admin':
        return user_controller.register_user_controller(data)
    return jsonify({"message":
                    "No permissions to add a user, should be admin"}), 401


@user.route('/api/v1/auth/login', methods=['POST'])
def login():
    """
    Logs in User
    """
    data = request.get_json()
    return user_controller.login_controller(data)

@user.route('/api/v1/recipients', methods=['GET'])
@jwt_required
def get_users():
    """
    Admin fetches all users
    """
    token = helper_controller.get_token_from_request()
    if user_controller.check_user_permission(token) == 'Loader' or\
            user_controller.check_user_permission(token) == 'Admin':
        all_recipients = user_controller.get_all_recipients()
        return jsonify({"Recipients": all_recipients})
    return jsonify({"message":
                    "Only Admin or Loader can view all Recipients"}), 401