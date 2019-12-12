import json
from cms.shopify.main import Shopify

class CMS():
    def __init__(self, vendor):
        if vendor['cms'] == 'shopify':
            self.cms = Shopify(vendor['url'])

def load_cms():
    with open('config/cms.json', 'r') as f:
        return json.load(f)
