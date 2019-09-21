from database_handler import DbConn
from werkzeug.security import generate_password_hash, check_password_hash

class UserController:
    """
    This interfaces with the database
    """
    def __init__(self):
        conn = DbConn()
        self.cur = conn.create_connection()
        conn.create_users_table()

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
