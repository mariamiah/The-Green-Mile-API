import re
import datetime


class PackageValidate:
    """This class contains validators for the different package inputs"""

    def validate_package_fields(self, data):
        # Validates package fields
        if len(data.keys()) != 10:
            return "Wrong number of fields, should be 10"
        try:
            for field in data.keys():
                if data[field] == "":
                    return field + " cannot be blank"
                if not isinstance(data[field], str):
                    return "Enter string value at {}".format(field)
        except KeyError:
            return "Invalid Key added"

    def validate_packages_regexes(self, data):
        package_fields = ['package_name', 'hub_address']
        for field in package_fields:
            if not re.match(r"([a-zA-Z_0-9 ]*$)", data[field]):
                return "Only alphanumerics allowed in {}".format(field)
            if re.match(r"([0-9])", data[field]):
                return "numbers only not allowed in {}".format(field)

    def validate_date_regex(self, data):
        try:
            datetime.datetime.strptime(data['delivery_date'], '%Y-%m-%d')
        except ValueError:
            return "Enter delivery_date in YYYY-MM-DD format"

    def compare_dates(self, data):
        date_created = datetime.datetime.now()
        delivery_date = datetime.datetime.strptime(
            data['delivery_date'], "%Y-%m-%d")
        if date_created > delivery_date:
            return "delivery date should be the recent date"

    def validate_date(self, data):
        return self.compare_dates(data)

    def validate_package(self, data):
        """
        validate the entire package
        """
     
        if isinstance(self.validate_package_fields(data), str):
            return self.validate_package_fields(data)
        if isinstance(self.validate_packages_regexes(data), str):
            return self.validate_packages_regexes(data)
        if isinstance(self.validate_date_regex(data), str):
            return self.validate_date_regex(data)
        if isinstance(self.compare_dates(data), str):
            return self.compare_dates(data)
        if self.validate_delivery_status(data):
            return "Status should either be preparing for shipment, shipped or delivered"
        return "valid package details"
    

    def validate_package_type(self, data):
        """
        Validates the package type field
        """
        if data['package_type_name'] == "":
            return "package_type_name cannot be blank"
        return "valid package type"

    def validate_loading_type_fields(self, data):
        # validates the loading type fields
        try:
            if len(data.keys()) != 1:
                return "Invalid number of keys"
            if not data["loading_type_name"]:
                return "Add the loading_type_name field"
            if self.check_load_type_fields(data):
                return "Load type name should be pallet, roll, container or box"
            if data['loading_type_name'] == "":
                return "loading_type_name cannot be blank"
            return "valid load type"
        except KeyError:
            return "Invalid key fields"

    def check_load_type_fields(self, data):
        if data['loading_type_name'].lower() != 'roll' and \
                data['loading_type_name'].lower() != 'pallet' and \
                data['loading_type_name'].lower() != 'box' and \
                data['loading_type_name'].lower() != 'container':
            return True
        return False
    
    def validate_delivery_status(self, data):
        if data["delivery_status"].lower() != "preparing for shipment" and \
            data["delivery_status"].lower() != "shipped" and \
            data["delivery_status"].lower() != "delivered":
            return True
        return False
