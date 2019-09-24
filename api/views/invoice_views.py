from flask import Flask, request, jsonify, Blueprint
from api.controllers.invoice_controllers import InvoiceController

invoice = Blueprint('invoice', __name__)
invoice_controller = InvoiceController()


@invoice.route('/api/v1/invoices', methods=['POST'])
def create_invoice():
    data = request.get_json()   
    return invoice_controller.create_new_invoice(data)
