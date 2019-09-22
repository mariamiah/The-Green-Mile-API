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
def register_package():
    """
    Registers a package
    """
    data = request.get_json()
    token = helper_controller.get_token_from_request()
    if user_controller.check_user_permission(token) == 'Supplier' or\
        user_controller.check_user_permission(token) == 'Admin':
        return package_controller.register_package(data)
    return jsonify({"message": "No permissions to add a package, should be supplier or admin"}), 401
    

