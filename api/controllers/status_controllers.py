from flask import jsonify
from database_handler import DbConn
from api.validators.status_validators import StatusValidate


status_validator = StatusValidate()

class Status:
    def __init__(self):
        conn = DbConn()
        self.cur = conn.create_connection()
        conn.create_status_table()
    
    def check_if_status_exists(self, data):
        sql = """SELECT * FROM status_table WHERE status_name= '{}'"""
        self.cur.execute(sql.format(data['status_name']))
        row = self.cur.fetchone()
        if row:
            return True

    def create_status(self, data):
        sql = """INSERT INTO status_table(status_name) VALUES ('{}')"""
        self.cur.execute(sql.format(data['status_name']))
    
    def add_status(self, data):
        if status_validator.validate_status(data):
            if not self.check_if_status_exists(data):
                self.create_status(data)
                return jsonify({"message": "status added successfully"}), 201
            return jsonify({"message": "status already exists"}), 400
        return jsonify({"message": status_validator.validate_status_fields(data)})
