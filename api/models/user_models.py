from flask import jsonify, request

class User:
    """
    This class describes the attributes of a user
    """
    def __init__(self, **kwargs):
        self.email= kwargs.get('email')
        self.username = kwargs.get('username')
        self.password=kwargs.get('password')
        self.confirm_password=kwargs.get('confirm_password')
        self.role=kwargs.get('role')
