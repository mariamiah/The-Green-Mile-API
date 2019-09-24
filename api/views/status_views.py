from flask import request, jsonify, Blueprint
from api.controllers.status_controllers import Status

status = Blueprint('status', __name__)
status_controller = Status()


@status.route('/api/v1/status', methods=['POST'])
def register_status():
    """
    Adds a shipment status
    """
    data = request.get_json()
    return status_controller.add_status(data)
