from flask import jsonify
from database_handler import DbConn
from api.validators.invoice_validators import InvoiceValidators


invoice_validator = InvoiceValidators()


class InvoiceController:
    def __init__(self):
        conn = DbConn()
        self.cur = conn.create_connection()
        conn.create_invoice_table()

    def add_invoice(self, data):
        sql = """INSERT INTO invoices(invoice_number, invoice_status) VALUES 
                 ('{}', '{}')"""
        self.cur.execute(sql.format(data['invoice_number'], data['invoice_status']))
    
    def create_new_invoice(self, data):
        is_valid = invoice_validator.valid_invoice_field(data)
        if is_valid == "is_valid":
            if not self.check_if_invoice_exists(data):
                self.add_invoice(data)
                return jsonify({"message": "invoice successfully created"}), 201
            return jsonify({"message": "invoice already exists"}), 400
        return jsonify({"message": is_valid}), 400
    
    def check_if_invoice_exists(self, data):
        sql = """SELECT * FROM invoices WHERE invoice_number= '{}'"""
        self.cur.execute(sql.format(data['invoice_number']))
        row = self.cur.fetchone()
        if row:
            return True
    

