import aiohttp, configparser, asyncio, json

config = configparser.ConfigParser()
config.read('config.ini')

class shopify():
    def __init__(self, url):
        self.products = dict()
        self.site = url
        self.uri = config['shopify']['dataloc']
        self.url = f"{self.site}{self.uri}"

    async def crawl(self):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.url) as r:
                    self.text = await r.text()
            except:
                print('oopsie woopsie')

    async def loadProducts(self):
        self.products = json.loads(self.text)['products']