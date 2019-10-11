from flask import Flask, request, jsonify, Blueprint
from api.controllers.invoice_controllers import InvoiceController

invoice = Blueprint('invoice', __name__)
invoice_controller = InvoiceController()

