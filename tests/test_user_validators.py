import unittest
from api.validators.user_validators import UserValidate
from api import app


class TestUserValidator(unittest.TestCase):
    """ Tests User validators """

    def setUp(self):
        """Sets up the validator class """
        self.validate = UserValidate()

    def test_validate_user_fields_if_fields_less(self):
        # Tests to ensure the correct data definition for the users passes
        data = {
            "password": "rtrkhWE1",
            "username": "mirembe",
            "email": "mirembe3@mail.com",
            "role": "Supplier"
        }
        self.assertEqual(self.validate.validate_user_fields(data),
                         "Wrong number of fields, should be 5")

    def test_blank_fields_validation(self):
        # Tests that the function will not pass if blank fields are provided
        data = {
            "password": "rtrkhWE1",
            "username": "",
            "email": "mirembe3@mail.com",
            "role": "Supplier",
            "confirm_password": "rtrkhWE1"
        }
        self.assertEqual(self.validate.validate_user_fields(data),
                         "username cannot be blank")

    def test_return_if_wrong_datatype(self):
        # Tests the return value if a wrong value is entered
        data = {
            "password": "rtrkhWE1",
            "username": "maria",
            "email": "mirembe3@mail.com",
            "role": 5,
            "confirm_password": "rtrkhWE1"
        }
        self.assertEqual(self.validate.validate_user_fields(data),
                         "Enter string value at role")

    def test_raises_exception(self):
        # tests an exception is raised if invalid fields are entered
        data = {
            "password": "rtrkhWE1",
            "username": "maria",
            "email": "mirembe3@mail.com",
            "role": "Admin",
            "confirmassword": "rtrkhWE1"
        }
        self.assertEqual(self.validate.validate_user_fields(data),
                         "Invalid Key added")
    
    def test_validate_email_regexes(self):
        # Tests an error is raised if wrong format data is entered
        data = {
            "password": "rtrkhWE1",
            "username": "maria",
            "email": "mirembe3mail.com",
            "role": "Admin",
            "confirm_password": "rtrkhWE1"
        }
        self.assertEqual(self.validate.validate_user_regexes(data),
                         "Invalid email format")
    
    def test_validate_unsimilar_passwords(self):
        # Tests an error is raised if a wrong password is provided
        data = {
            "password": "rtr",
            "username": "maria",
            "email": "mirembe3@mail.com",
            "role": "Admin",
            "confirm_password": "rtr#DSDSDSS"
        }
        self.assertEqual(self.validate.validate_user_password(data),
                         "passwords dont match")
