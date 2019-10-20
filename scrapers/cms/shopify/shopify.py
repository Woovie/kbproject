import aiohttp, configparser, asyncio, json, pprint

config = configparser.ConfigParser()
config.read('config.ini')

class shopify():
    def __init__(self, url):
        self.products = []
        self.site = url
        self.storeuri = config['shopify']['dataloc']
        self.storeurl = f"{self.site}{self.storeuri}"
        self.producturi = config['shopify']['itemloc']
        self.producturl = f"{self.site}{self.producturi}"

    async def crawl(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.storeurl) as r:
                if r.status == 200:
                    self.text = await r.text()
                else:
                    print(f"[ERROR] Request returned unexpected value: Status {r.status}, expected 200")

    async def loadProducts(self):
        products = json.loads(self.text)['products']
        for product in products:
            self.products.append({'name': product['title'], 'url': f"{self.producturl}{product['product_id']}"})
