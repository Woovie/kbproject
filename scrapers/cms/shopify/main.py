import aiohttp, configparser, oembed, asyncio

config = configparser.ConfigParser()
config.read('config.ini')

class shopify():
    def __init__(self, url):
        self.products = dict()
        self.site = url
        self.uri = config['shopify']['dataloc']
        self.url = f"{self.site}{self.uri}"

    async def crawl():
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as r:
                print(r)

shopify = shopify('https://dailyclack.com')
asyncio.run(shopify.crawl())