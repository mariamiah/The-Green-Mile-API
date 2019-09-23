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
