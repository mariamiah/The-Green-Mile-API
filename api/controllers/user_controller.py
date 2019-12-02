from database_handler import DbConn
from werkzeug.security import generate_password_hash, check_password_hash
from api.validators.user_validators import UserValidate
from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    get_jwt_claims
)
from datetime import datetime, timedelta
from decouple import config
validate = UserValidate()


class UserController:
    """
    This user controller interfaces with the database
    """

    def __init__(self):
        conn = DbConn()
        self.cur = conn.create_connection()
        conn.create_users_table()
        conn.create_default_admin()

    def check_email_exists(self, email):
        """
        Checks if the email already exists
        """
        sql = """SELECT * from users where email = '{}'"""
        self.cur.execute(sql.format(email))
        row = self.cur.fetchall()
        if row:
            return True

    def check_if_username_exists(self, username):
        """
        checks if the username is already in the database
        """
        sql = """SELECT * from users where username='{}'"""
        self.cur.execute(sql.format(username))
        row = self.cur.fetchall()
        if row:
            return True

    def check_if_user_exists(self, data):
        """
        Checks if the user exists in the database to authorize login

        """
        sql = """SELECT * from users where username = '{}'"""
        self.cur.execute(sql.format(data['username']))
        row = self.cur.fetchall()
        if row:
            return True

    def check_password(self, data):
        """
        Checks the password hash
        """
        data = request.get_json()
        sql = """SELECT password FROM users WHERE username='{}'"""
        self.cur.execute(sql.format(data['username']))
        row = self.cur.fetchone()
        if check_password_hash(row[0], data['password']):
            return True
        return False

    def create_user(self, data):
        """
        Creates a user
        """
        hashed_password = generate_password_hash(data['password'], 'sha256')
        sql = """INSERT INTO users(email, username, password, role)
                        VALUES ('{}', '{}', '{}', '{}')"""
        sql_command = sql.format(data['email'],
                                 data['username'],
                                 hashed_password,
                                 data['role'])
        self.cur.execute(sql_command)

    def get_role(self):
        data = request.get_json()
        sql = """SELECT role FROM users WHERE username = '{}'"""
        self.cur.execute(sql.format(data['username']))
        role = self.cur.fetchone()
        if role:
            return role

    def check_user_permission(self, token):
        identity = get_jwt_identity()
        fetched_role = identity['role']
        roles = ['Admin', 'Supplier', 'Recipient', 'Loader']
        for role in roles:
            if role == fetched_role[0]:
                return role

    def generate_login_token(self, data):
        """
        Assigns access token to user
        """
        data = request.get_json()
        role = self.get_role()
        identity = {
            'username': data['username'],
            'role': role
        }
        expires = timedelta(hours=23)
        access_token = create_access_token(identity=identity,
                                           expires_delta=expires)
        return jsonify(access_token=access_token), 200

    def register_user_controller(self, data):
        is_valid = validate.validate_user(data)

        if is_valid == "is_valid":
            if not self.check_email_exists(data['email']):
                if not self.check_if_username_exists(data['username']):
                    self.create_user(data)
                    return jsonify({"message":
                                    "user successfully created"}), 201
                return jsonify({"message": "Username already exists"}), 400
            return jsonify({"message": "Email already exists"}), 400
        
        return jsonify({"message": is_valid}), 400

    def login_controller(self, data):
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        login_valid = validate.validate_login(data)
        if login_valid == "valid login fields":
            if self.check_if_user_exists(data):
                if self.check_password(data):
                    return self.generate_login_token(data)
                return jsonify({"message": "Enter correct password"}), 400
            return jsonify({"message":
                            "Username doesnot exist, please register with Admin"}), 400
        return jsonify({"message": login_valid})
