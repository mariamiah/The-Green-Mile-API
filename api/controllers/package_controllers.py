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

    def get_user_name(self, token):
        """
        Obtain the supplier name from the token
        """
        identity = get_jwt_identity()
        user_name = identity['username']
        return user_name

    def execute_sql(self, data):
        tables = ['package_type', 'loading_type', 'invoices', 'status_table']
        columns = ['package_type_name', 'loading_type_name', 'invoice_number',
                   'status_name']
        values = [data['package_type'], data['loading_type_name'],
                  data['invoice_number'], data['delivery_status']]
        for table, column, value in zip(tables, columns, values):
            sql_command = helper_controller.query_database_details(table,
                                                                   column,
                                                                   value)
            self.cur.execute(sql_command)
            row = self.cur.fetchone()
            if row is None:
                return("{} doesnot exist in {} table".format(value, table))

    def create_package(self, data):
        """
        Creates package details in the database
        """
        token = helper_controller.get_token_from_request()
        supplier_name = self.get_user_name(token)
        sql = """INSERT INTO packages(package_name, package_type_name,
                                      delivery_description, loading_type_name,
                                      hub_address, recipient_address,
                                      supplier_name, recipient_name,
                                      invoice_number, delivery_date,
                                       delivery_status) VALUES ('{}', '{}',
                                                                '{}', '{}',
                                                                '{}','{}',
                                                                '{}','{}','{}',
                                                                '{}', '{}')"""
        sql_command = sql.format(data['package_name'], data['package_type'],
                                 data['delivery_description'],
                                 data['loading_type_name'],
                                 data['hub_address'],
                                 data['recipient_address'], supplier_name,
                                 data['recipient_name'],
                                 data['invoice_number'],
                                 data['delivery_date'],
                                 data['delivery_status'])
        self.cur.execute(sql_command)

    def check_if_recipient_exists(self, data):
        sql = """ SELECT * FROM users WHERE username = '{}' and role='{}'"""
        sql_command = sql.format(data['recipient_name'], 'Recipient')
        self.cur.execute(sql_command)
        row = self.cur.fetchall()
        if row:
            return True

    def register_package(self, data):
        package_valid = package_validate.validate_package(data)
        if package_valid == "valid package details":
            if not isinstance(self.execute_sql(data), str):
                if self.check_if_recipient_exists(data):
                    self.create_package(data)
                    return jsonify(
                        {"message": "Package created successfully"}), 201
                return jsonify(
                    {"message":
                     "Either user doesnot exist or not Recipient"}), 404
            return jsonify({"message": self.execute_sql(data)}), 404
        return jsonify({"message": package_valid})

    def return_package_fields(self, rows):
        packages = []
        for row in rows:
            packages.append({
                "package_id": row[0],
                "package_name": row[1],
                "package_type": row[2],
                "delivery_description": row[3],
                "loading_type_name": row[4],
                "hub_address": row[5],
                "recipient_address": row[6],
                "supplier_name": row[7],
                "recipient_name": row[8],
                "invoice_number": row[9],
                "date_registered": row[10],
                "delivery_date": row[11],
                "delivery_status": row[12]
            })
        return packages

    def fetch_packages(self):
        sql = """ SELECT * FROM packages"""
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        return self.return_package_fields(rows)

    def fetch_single_packages(self, username):
        rows = self.cur.fetchall()
        return self.return_package_fields(rows)

    def fetch_user_packages(self, username):
        sql = """ SELECT * FROM packages WHERE recipient_name = '{}'"""
        self.cur.execute(sql.format(username))
        return self.fetch_single_packages(username)

    def fetch_supplier_packages(self, username):
        sql = """ SELECT * FROM packages WHERE supplier_name = '{}'"""
        self.cur.execute(sql.format(username))
        return self.fetch_single_packages(username)

    def fetch_single_package(self, id):
        package = []
        sql = """ SELECT * FROM packages WHERE package_id = '{}'"""
        self.cur.execute(sql.format(id))
        row = self.cur.fetchone()
        if row:
            package.append({
                "package_id": row[0],
                "package_name": row[1],
                "package_type": row[2],
                "delivery_description": row[3],
                "loading_type_name": row[4],
                "hub_address": row[5],
                "recipient_address": row[6],
                "supplier_name": row[7],
                "recipient_name": row[8],
                "invoice_number": row[9],
                "date_registered": row[10],
                "delivery_date": row[11],
                "delivery_status": row[12]
            })
        return package
    
    def check_if_package_type_exists(self,data):
        sql = """SELECT * FROM package_type WHERE package_type_name = '{}'"""
        self.cur.execute(sql.format(data['package_type_name']))
        row = self.cur.fetchone()
        if row:
            return True
    
    def create_package_type(self, data):
        sql = """INSERT INTO package_type(package_type_name)VALUES('{}')"""
        self.cur.execute(sql.format(data['package_type_name']))

    def create_package_type_name(self, data):
        is_valid = package_validate.validate_package_type(data)
        if is_valid == "valid package type":
            if not self.check_if_package_type_exists(data):
                self.create_package_type(data)
                return jsonify({"message": "Package type succesfully created"}), 201
            return jsonify({"message": "Package already exists, try another"}), 400
        return jsonify({"message": is_valid}), 400