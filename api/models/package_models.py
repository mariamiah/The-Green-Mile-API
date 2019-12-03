class Package:
    """
    Defines the attributes of the package class
    """
    def __init__(self, **kwargs):
        self.package_name = kwargs.get('package_name')
        self.package_type = kwargs.get('package_type')
        self.delivery_description = kwargs.get('delivery_description')
        self.loading_type = kwargs.get('loading_type')
        self.hub_address = kwargs.get('hub_address')
        self.recipient_address = kwargs.get('recipient_address')
        self.recipient_name = kwargs.get('recipient_name')
        self.delivery_date = kwargs.get('delivery_date'),
        self.package_status = kwargs.get('delivery_status'),
        self.recipient_email = kwargs.get('recipient_email')
