import re

class UserValidate:
    """This class contains validators for the different inputs"""

    def validate_user_fields(self, data):
        # Validates user fields
        user_fields = ['email', 'password', 'username', 'role', 'confirm_password']
        if len(data.keys()) != 5:
            return "Wrong number of fields, should be 5"
        try:
            for user_field in user_fields:
                if data[user_field] == "":
                    return user_field + " cannot be blank"
                if not isinstance(data[user_field], str):
                    return "Enter string value at {}".format(user_field)
        except KeyError:
            return "Invalid Key added"
    def validate_user_regexes(self, data):
        if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)",
                        data['email']):
            return "Invalid email format"
        if not re.match(r"(?=^.{6,15}$)(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?!.*\s).*$",
                         data['password']):
            return "Enter password between 6-15 values, lowercase and uppercase alphanumerics, no spaces allowed"

        if not re.match(r"([a-zA-Z0-9]*$)", data['username']):
            return "Only alphanumerics allowed in user name"

        if re.match(r"([0-9])", data['username']):
            return "user name cannot contain numbers only"
    
    def validate_user_password(self, data):

        if data['password'] != data['confirm_password']:
            return "passwords dont match"

    def validate_user_role(self, data):
        if data['role'] != 'Admin' and data['role'] != 'Attendant':
            return "Role must be either Admin or Attendant"
    
    def validate_user(self, data):
        if isinstance(self.validate_user_fields(data), str):
            return self.validate_user_fields(data)
        if isinstance(self.validate_user_regexes(data), str):
            return self.validate_user_regexes(data)
        if isinstance(self.validate_user_password(data), str):
            return self.validate_user_password(data)
        if isinstance(self.validate_user_role(data), str):
            return self.validate_user_role(data)
        return "is_valid"
