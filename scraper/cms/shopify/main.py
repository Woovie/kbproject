import configparser, logging, re, json
from crawl import crawl
from configparser import ConfigParser

config = ConfigParser()
config.read('config/cms.ini')

logger = logging.getLogger('scraperMain')

class Shopify():
    def __init__(self, url):
        self.products = []
        self.url = f"{url}{config['shopify']['data_location']}"
        self.vendor = None

    async def load(self):
        resp = await crawl(self.url)
        self.products = json.loads(resp)['products']

    async def parse(self):
        products = []
        for product in self.products:
            product_dict = {}
            price_format = re.compile(r"(\d{1,3}\,){0,3}\d{1,3}(\.\d{2})?")
            product_dict['url'] = f"{self.vendor.url}{config['shopify']['product_prefix']}{product['handle']}"
            product_dict['name'] = product['title']
            if product['images']:
                product_dict['image'] = product['images'][0]['src']
            product_dict['variants'] = []
            for variant in product['variants']:
                variant_dict = {}
                variant_dict['name'] = variant['title']
                if variant['featured_image']:
                    variant_dict['image'] = variant['featured_image']['src']
                variant_dict['stock'] = variant['available']
                variant_dict['price'] = variant['price']
                product_dict['variants'].append(variant_dict)
            products.append(product_dict)
        self.vendor.products = products
