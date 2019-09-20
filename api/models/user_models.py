from database_handler import DbConn
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    """
    This class describes the attributes of a user
    """
    def __init__(self):
        self.user_id = 0
        self.email=""
        self.username = ""
        self.password=""
        self.role=""
        conn = DbConn()
        self.cur = conn.create_connection()
        conn.create_users_table()

    def create_user(self, data):
        hashed_password = generate_password_hash(data['password'], 'sha256')
        sql = """INSERT INTO users(email, username, password, role)
                            VALUES ('{}', '{}', '{}', '{}')"""
        sql_command = sql.format(data['email'],
                                 data['username'],
                                 hashed_password,
                                 data['role'])
        self.cur.execute(sql_command)

    