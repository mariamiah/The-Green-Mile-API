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
        package_fields = ['package_name', 'hub_address',
                          'recipient_address']
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
        delivery_date = datetime.datetime.strptime(data['delivery_date'], "%Y-%m-%d")
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
        return "valid package details"
