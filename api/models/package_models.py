class Package:
    """
    Defines the attributes of the package class
    """
    def __init__(self, **kwargs):
        self.package_name = kwargs.get('package_name')
        self.package_type = kwargs.get('package_type')
        self.delivery_description = kwargs.get('delivery_description')
        self.loading_type = kwargs.get('loading_type')
        self.source_address = kwargs.get('source_address')
        self.destination_address = kwargs.get('destination_address')
        self.supplier_name = kwargs.get('supplier_name')
        self.recipient_name = kwargs.get('recipient_name')
        self.invoice_number = kwargs.get('invoice_number')

