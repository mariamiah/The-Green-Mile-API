from flask import request, jsonify, Blueprint
from api.controllers.user_controller import UserController
from api.validators.user_validators import UserValidate

user = Blueprint('user', __name__)
user_controller = UserController()
validate = UserValidate()

@user.route('/api/v1/auth/signup', methods=['POST'])
def register_user():
    """
    Registers a User
    """
    data = request.get_json()
    is_valid = validate.validate_user(data)
    if is_valid == "is_valid":      
        if not user_controller.check_email_exists(data['email']):
            if not user_controller.check_if_username_exists(data['username']):
                user_controller.create_user(data)
                return jsonify({"message": "user successfully created"}), 201
            return jsonify({"message":"Username already exists"}), 400
        return jsonify({"message":"Email already exists"}), 400      
    return jsonify({"message": is_valid}), 400

