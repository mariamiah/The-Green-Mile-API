from flask import request, jsonify, Blueprint
from api.controllers.package_controllers import PackageController
from api.controllers.user_controller import UserController
from api.controllers.helper_controllers import HelperController
from flask_jwt_extended import jwt_required

package = Blueprint('package', __name__)
package_controller = PackageController()
user_controller = UserController()
helper_controller = HelperController()


@package.route('/api/v1/packages', methods=['POST'])
@jwt_required
def create_package():
    """
    Registers a package
    """
    data = request.get_json()
    token = helper_controller.get_token_from_request()
    if user_controller.check_user_permission(token) == 'Supplier' or\
       user_controller.check_user_permission(token) == 'Admin':
        return package_controller.register_package(data)
    return jsonify({"message":
                    "No permissions to add a package, should be supplier or admin"}), 401


@package.route('/api/v1/packages', methods=['GET'])
@jwt_required
def read_all_packages():
    """
    Displays all packages
    """
    token = helper_controller.get_token_from_request()
    if user_controller.check_user_permission(token) == 'Admin':
        all_packages = package_controller.fetch_packages()
        return jsonify({"Packages": all_packages})
    return jsonify({"message":
                    "Only Admin can view all packages"}), 401


@package.route('/api/v1/packages/recipient_packages', methods=['GET'])
@jwt_required
def read_recipient_packages():
    """
    Displays only packages specific to a recipient
    """
    token = helper_controller.get_token_from_request()
    username = package_controller.get_user_name(token)
    if user_controller.check_user_permission(token) == 'Recipient':
        my_packages = package_controller.fetch_user_packages(username)
        if my_packages:
            return jsonify({"my_packages": my_packages})
        return jsonify({"message": "You dont have any packages yet"}), 200
    return jsonify({"message": "Only accessed by Recipients"}), 401


@package.route('/api/v1/packages/supplier_packages', methods=['GET'])
@jwt_required
def read_supplier_packages():
    """
    Displays all packages of the supplier
    """
    token = helper_controller.get_token_from_request()
    username = package_controller.get_user_name(token)
    if user_controller.check_user_permission(token) == 'Supplier':
        supplier_packages = package_controller.fetch_supplier_packages(username)
        if supplier_packages:
            return jsonify({"message": supplier_packages})
        return jsonify({"message": "No created packages yet"}), 200
    return jsonify({"message": "Only accessed by suppliers"}), 401
