import aiohttp, configparser, asyncio, bs4

config = configparser.ConfigParser()
config.read('config.ini')

class shopify():
    def __init__(self, url):
        self.productsBS = []
        self.products = []
        self.site = url
        self.initStoreURI = config['shopify']['dataloc']
        self.productURI = config['shopify']['itemloc']

    async def parseStorePage(self, url):
        print(url)
        resp = await crawl(url)
        resp = bs4.BeautifulSoup(resp, 'html5lib')
        self.productsBS.extend(resp.find_all(class_='product-card'))
        nextPage = resp.find(rel='next')
        if nextPage:
            await self.parseStorePage(f"{self.site}{nextPage.get('href')}")

    async def loadProducts(self):
        for product in self.productsBS:
            productArray = {}
            uri = product.get('href')
            productArray['uri'] = uri
            productArray['url'] = f"{self.site}{uri}"
            productArray['name'] = product.find(class_="product-card__name").text
            price = product.find(class_="product-card__price")
            soldOut = product.find(class_="product-card__availability")
            if soldOut:
                productArray['price'] = "None"
                productArray['availability'] = False
            else:
                productArray['price'] = " ".join(price.text.split()).replace("Regular price ", "").replace("From ", "")
                productArray['availability'] = True
            self.products.append(productArray)


async def crawl(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 200:
                return await r.text()
            else:
                raise ResponseError(f"[ERROR] GET {url} returned unexpected value: {r.status} {r.reason}, expected 200 OK")
