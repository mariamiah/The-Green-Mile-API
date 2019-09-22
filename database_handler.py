import os
import psycopg2
from werkzeug.security import generate_password_hash
from decouple import config


class DbConn:
    def create_connection(self):
        """ Function that creates the database based on the application
            environment"""
        if os.environ.get('APP_SETTINGS') == 'testing':
            self.conn = psycopg2.connect(config("TEST_DATABASE_URL"))
        elif os.environ.get('APP_SETTINGS') == 'production':
            self.conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
        else:
            self.conn = psycopg2.connect(config("DATABASE_URL"))
        self.conn.autocommit = True
        self.cur = self.conn.cursor()
        return self.cur

    def create_users_table(self):
        """A function to create the users table"""
        self.cur.execute('''CREATE TABLE IF NOT EXISTS users
            (user_id  SERIAL PRIMARY KEY  NOT NULL,
            email VARCHAR(250) NOT NULL UNIQUE,
            username VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(100) NOT NULL,
            role VARCHAR(100) NOT NULL); ''')

    def create_package_types_table(self):
        """ Creates the package types table """
        self.cur.execute('''CREATE TABLE IF NOT EXISTS package_type
             (package_type_id SERIAL PRIMARY KEY NOT NULL,
              package_type_name VARCHAR(250) NOT NULL UNIQUE
            );''')

    def create_loading_types_table(self):
        """ Creates the loading types table """
        self.cur.execute(''' CREATE TABLE IF NOT EXISTS loading_type
        (loading_type_id SERIAL PRIMARY KEY NOT NULL,
         loading_type_name VARCHAR(100) NOT NULL UNIQUE
        );''')

    def create_status_table(self):
        """ Creates the status table """
        self.cur.execute(''' CREATE TABLE IF NOT EXISTS status_table
        (status_id SERIAL PRIMARY KEY NOT NULL,
        status_name VARCHAR(50) NOT NULL UNIQUE)''')

    def create_invoice_table(self):
        """ Creates the invoice table """
        self.cur.execute(''' CREATE TABLE IF NOT EXISTS invoices
        (invoice_id SERIAL PRIMARY KEY NOT NULL,
        invoice_number VARCHAR(100) NOT NULL UNIQUE,
        invoice_status VARCHAR(100) REFERENCES status_table(status_name) ON\
               DELETE CASCADE
         );''')

    def create_packages_table(self):
        """ A function that creates the packages table """
        self.cur.execute('''CREATE TABLE IF NOT EXISTS packages
        (package_id SERIAL PRIMARY KEY NOT NULL,
         package_name VARCHAR(250) NOT NULL,
         package_type_name VARCHAR(100)\
         REFERENCES package_type(package_type_name) ON\
                      DELETE CASCADE,
         delivery_description VARCHAR(500) NOT NULL,
         loading_type_name VARCHAR(100)\
         REFERENCES loading_type(loading_type_name) ON\
                      DELETE CASCADE,
         source_address VARCHAR(250) NOT NULL,
         destination_address VARCHAR(250) NOT NULL,
         supplier_name VARCHAR(250) NOT NULL,
         recipient_name VARCHAR(255) REFERENCES users(username) ON\
                     DELETE CASCADE,
         invoice_number VARCHAR REFERENCES invoices(invoice_number) ON\
                     DELETE CASCADE,
         date_created DATE NOT NULL DEFAULT CURRENT_DATE,
         delivery_date DATE NOT NULL,
         delivery_status VARCHAR(100) REFERENCES status_table(status_name) ON\
                    DELETE CASCADE
         );''')

    def close_DB(self):
        self.conn.commit()
        self.conn.close()
