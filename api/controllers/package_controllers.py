from database_handler import DbConn
from flask import request, jsonify
from decouple import config
from flask_jwt_extended import get_jwt_identity
from api.validators.package_validators import PackageValidate
from api.controllers.helper_controllers import HelperController
import psycopg2


package_validate = PackageValidate()
helper_controller = HelperController()
class PackageController:
    """
    This package controller interfaces with the database
    """
    def __init__(self):
        conn = DbConn()
        self.cur = conn.create_connection()
        conn.create_package_types_table()
        conn.create_loading_types_table()
        conn.create_users_table()
        conn.create_status_table()
        conn.create_invoice_table()
        conn.create_packages_table()

    def get_supplier_name(self, token):
        """
        Obtain the supplier name from the token
        """
        identity = get_jwt_identity()
        supplier_name = identity['username']
        return supplier_name

    def execute_sql(self, data):
        tables = ['package_type', 'loading_type', 'invoices','status_table']
        columns = ['package_type_name','loading_type_name', 'invoice_number', 'status_name']
        values = [data['package_type'],data['loading_type_name'],data['invoice_number'], data['delivery_status']]
        for table, column, value in zip(tables, columns, values):
            sql_command = helper_controller.query_database_details(table, column, value)
            self.cur.execute(sql_command)
            row = self.cur.fetchone()
            if row is None:
                return("{} doesnot exist in {} table".format(value, table))
 
    def create_package(self, data):
        """
        Creates package details in the database
        """
        token = helper_controller.get_token_from_request()
        supplier_name = self.get_supplier_name(token)
        sql = """INSERT INTO packages(package_name, package_type_name, delivery_description, loading_type_name,\
                                      source_address, destination_address, supplier_name, recipient_name, invoice_number,\
                                       delivery_status) VALUES ('{}', '{}', '{}', '{}', '{}','{}','{}','{}','{}','{}')"""
        sql_command = sql.format(data['package_name'], data['package_type'], data['delivery_description'], data['loading_type_name'],
                                 data['source_address'], data['destination_address'], supplier_name, data['recipient_name'],
                                 data['invoice_number'],data['delivery_status'])
        self.cur.execute(sql_command)
    
 
    def check_if_recipient_exists(self, data):
        sql = """ SELECT * FROM users WHERE username = '{}' and role='{}'"""
        sql_command = sql.format(data['recipient_name'], 'Recipient' )
        self.cur.execute(sql_command)
        row = self.cur.fetchall()
        if row:
            return True

    def register_package(self, data):
        package_valid = package_validate.validate_package(data) 
        if package_valid== "valid package details":
            if not isinstance(self.execute_sql(data), str):
                if self.check_if_recipient_exists(data):
                    self.create_package(data)
                    return jsonify({"message": "Package created successfully"}), 201
                return jsonify({"message": "Either user doesnot exist or is not registered as Recipient"}),404
            return jsonify({"message": self.execute_sql(data)}), 404
        return jsonify({"message": package_valid})