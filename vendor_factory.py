import json
import vendor

class Vendors():
    def __init__(self, vendors_file: str):
        self.vendors_file = vendors_file
        self.vendors = []

    def load(self):
        with open(self.vendors_file, "r") as json_data:
            self.vendors = json.load(json_data)

    def build_vendors(self):
        for vendor in self.vendors:
            self.build_vendor(vendor)

    def build_vendor(self, vendor_dict: dict) -> vendor.Vendor:
        if vendor_dict["cms"] == "Shopify":
            return shopify.ShopifyVendor(vendor_dict)
