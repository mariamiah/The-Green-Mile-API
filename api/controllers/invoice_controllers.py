from flask import jsonify
from database_handler import DbConn
from api.validators.invoice_validators import InvoiceValidators
from api.controllers.package_controllers import PackageController
from api.controllers.helper_controllers import HelperController

invoice_validator = InvoiceValidators()
helper_controller = HelperController()
package_controller = PackageController()

class InvoiceController:
    def __init__(self):
        conn = DbConn()
        self.cur = conn.create_connection()
        conn.create_packages_table()
        conn.create_invoice_table()

    def add_supplier_invoice(self, data):
        token = helper_controller.get_token_from_request()
        invoice_number = 1
        invoice_owner = package_controller.get_user_name(token)
        invoice_status = "pending"
        sql = """INSERT INTO invoices(invoice_number, invoice_status, invoice_owner) VALUES 
                 ('{}', '{}', '{}')"""
        self.cur.execute(sql.format(invoice_number, invoice_status, invoice_owner))
    
    def create_new_invoice(self, data):
        is_valid = invoice_validator.valid_invoice_field(data)
        if is_valid == "is_valid":
            if not self.check_if_invoice_exists(data):
                self.add_supplier_invoice(data)
                return jsonify({"message": "invoice successfully created"}), 201
            return jsonify({"message": "invoice already exists"}), 400
        return jsonify({"message": is_valid}), 400
    
    def check_if_invoice_exists(self, data):
        sql = """SELECT * FROM invoices WHERE invoice_number= '{}'"""
        self.cur.execute(sql.format(data['invoice_number']))
        row = self.cur.fetchone()
        if row:
            return True
    

