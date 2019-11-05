import configparser, bs4, logging, re
from crawl import crawl

logger = logging.getLogger('scraperMain')

config = configparser.ConfigParser()
config.read('config.ini')

# Vendor class
# class vendor():
#     def __init__(self, name, url, cms, active):
#         self.products = []
#         self.name = name
#         self.url = url
#         self.cms = cms
#         self.active = active

# [shopify]
# dataloc=/collections/all
# itemloc=/products/

# parseStorePage notes:
# There's many different possibilities with how items may
# be rendered, so we are going to do multiple class
# selectors and add cases for vendors as we come along them

selectors = [
    'product-card',
    'grid-product__wrapper',
    'productitem',
    'grid-product__grid-item',
    'product',
    'product-grid-item'
]

class shopify():
    def __init__(self, url):
        self.products = []
        self.url = url
        self.firstURI = config['shopify']['dataloc']
        self.productURI = config['shopify']['itemloc']

    async def parseStorePage(self, url):
        resp = await crawl(url)
        resp = bs4.BeautifulSoup(resp, 'html.parser')
        selectTry = None
        for selector in selectors:
            selectTry = resp.find_all(class_=selector)
            if len(selectTry) > 0:
                break
        if selectTry:
            self.products.extend(selectTry)
            nextPage = resp.find(rel='next')
            if nextPage:
                await self.parseStorePage(f"{self.url}{nextPage.get('href')}")
        elif not selectTry and len(self.products) == 0:
            logger.debug(f"No products found for {self.url}")

async def loadProducts(vendor):
    prodDict = []
    for product in vendor.cms.products:
        productArray = {}
        productClass = product.get('class')
        if 'product-card' in productClass:# Daily Clack, Little Keyboards, Teal Technik
            #URL
            url = None
            if product.name == 'a':
                url = product.get('href')
            else:
                url = product.find('a').get('href')
            productArray['url'] = url
            #Name
            name = None
            nameClasses = [
                'product-card__name',
                'product-card__title'
            ]
            for nameClass in nameClasses:
                if product.find(class_=nameClass):
                    name = product.find(class_=nameClass).contents[0]
                    break
            productArray['name'] = name
            image = None
            if (foundImage := product.find(class_='product-card__image')):
                image = foundImage
            elif (foundImage := product.find(class_='grid-view-item__image')):
                image = foundImage
            else:
                image = 'http://woovie.net/404.jpg'
            productArray['image'] = image
            price = None
            stock = None
            if foundPrice := product.find(class_='product-card__price'):
                if len(foundPrice.contents) == 3:
                    price = foundPrice.contents[2]
                else:
                    price = foundPrice.contents[0]
                stock = True
            elif foundStock := product.find(class_='product-card__availability'):
                price = '0.00'
                stock = False
            if not price and not stock:# Not daily clack
                priceItem = product.find(class_='price-item--regular').contents
                if "Sold out" in priceItem:
                    price = '0.00'
                    stock = False
                else:
                    price = priceItem
                    stock = True
            productArray['price'] = price
            productArray['stock'] = stock
        elif 'grid-product__wrapper' in productClass:#  iLumkb
            productArray['url'] = product.find('a').get('href')
            productArray['name'] = product.find(class_='grid-product__title').contents[0]
        elif 'productitem' in productClass:# deskhero
            productArray['url'] = product.find('a').get('href')
            productArray['name'] = product.find(class_='productitem--title').a.contents[0]
        elif 'grid-product__grid-item' in productClass:#TheKeyCompany
            productArray['url'] = product.find('a').get('href')
            productArray['name'] = product.find(class_='grid-product__title').contents[0]
        elif 'product' in productClass:# MKUltra
            productArray['url'] = product.find('a').get('href')
            productArray['name'] = product.find(class_='product__title').a.contents[0]
        elif 'product-grid-item' in productClass:# Switchmod
            productArray['url'] = product.get('href')
            productArray['name'] = product.p.contents[0]
        #Name filtering should be done down here to remove characters like `\n` and spaces from the start and end of the name
        prodDict.append(productArray)
    return prodDict
