class InvoiceValidators:
    def validate_invoice_fields(self, data):
        if len(data.keys()) != 2:
            return "Wrong number of fields, should be 2"
        try:
            for field in data.keys():
                if data[field] == "":
                    return field + " cannot be blank"
                if not isinstance(data[field], str):
                    return "Enter string value at {}".format(field)
        except KeyError:
            return "Invalid Key added"

    def valid_invoice_field(self, data):
        if isinstance(self.validate_invoice_fields(data), str):
            return self.validate_invoice_fields(data)
        return "is_valid"