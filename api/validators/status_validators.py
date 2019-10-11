import re


class StatusValidate:
    """This class contains validators for the different status inputs"""

    def validate_status_fields(self, data):
        # Validates package fields
        if len(data.keys()) != 1:
            return "Wrong number of fields, should be 1"
        if data["status_name"] == "":
            return "status name cannot be blank"
        if not isinstance(data["status_name"], str):
                return "Enter string value"
        return "valid"


    def validate_status(self, data):
        """
        validate all the status fields
        """
        msg = self.validate_status_fields(data)
        try:
            if msg == "valid":
                return True
            return False
        except KeyError:
            return "Invalid key added"

  
