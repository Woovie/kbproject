import configparser, bs4, logging, re
from csv import reader
from crawl import crawl

logger = logging.getLogger('scraperMain')

config = configparser.ConfigParser()
config.read('config/cms.ini')

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
    'grid-view-item__link'
]

class shopify():
    def __init__(self, url):
        self.products = []
        self.url = url
        self.selector = None
        self.firstURI = config['shopify']['dataloc']
        self.productURI = config['shopify']['itemloc']

    async def parseStorePage(self, url):
        resp = await crawl(url)
        resp = bs4.BeautifulSoup(resp, 'html.parser')
        selectTry = None
        if self.selector:
            selectTry = resp.find_all(class_=self.selector)
        else:
            for selector in selectors:
                selectTry = resp.find_all(class_=selector)
                if len(selectTry) > 0:
                    self.selector = selector
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
        priceFormat = re.compile(r"(\d{1,3}\,){0,3}\d{1,3}(\.\d{2})?")
        url = None
        name = None
        image = None
        price = None
        stock = None
        # Daily Clack, Little Keyboards, Teal Technik
        if 'product-card' in productClass:
            logger.debug(f"{vendor.name} product-card")
            # URL
            if product.name == 'a':
                url = product.get('href')
            else:
                url = product.find('a').get('href')
            productArray['url'] = url
            # Name
            nameClasses = [
                'product-card__name',
                'product-card__title'
            ]
            for nameClass in nameClasses:
                if product.find(class_=nameClass):
                    name = product.find(class_=nameClass).contents[0]
                    break
            productArray['name'] = name
            # Image
            if (foundImage := product.find(class_='product-card__image')):
                image = foundImage.get('src')
            elif (foundImage := product.find(class_='grid-view-item__image')):
                if foundImage.name == 'img':
                    image = foundImage.get('data-src').format(width=2048)
            else:
                image = 'http://woovie.net/404.jpg'
            productArray['image'] = image
            # Price and stock
            if priceTag := product.find(class_='product-card__price'):
                if len(priceTag.contents) == 3:
                    price = priceTag.contents[2]
                else:
                    price = priceTag.contents[0]
                stock = True
            elif foundStock := product.find(class_='product-card__availability'):
                price = '0.00'
                stock = False
            if not price and not stock:# Not daily clack
                priceItem = product.find(class_='price-item--regular').contents
                if "Sold out" in priceItem[0]:
                    price = '0.00'
                    stock = False
                else:
                    price = priceFormat.search(priceItem[0])[0]
                    stock = True
            productArray['price'] = price
            productArray['stock'] = stock
        # iLumkb
        elif 'grid-product__wrapper' in productClass:
            logger.debug(f"{vendor.name} grid-product__wrapper")
            # URL
            productArray['url'] = product.find('a').get('href')
            # Name
            productArray['name'] = product.find(class_='grid-product__title').contents[0]
            # Image
            productArray['image'] = product.find(class_='grid-product__image').get('src')
            # Price and stock
            priceTag = product.find(class_='grid-product__price')
            if match := priceFormat.search(priceTag.contents[2]):
                price = match[0]
                stock = True
            elif match := priceFormat.search(priceTag.contents[4]):
                price = match[0]
                stock = True
            else:
                price = "0.00"
                stock = False
            productArray['price'] = price
            productArray['stock'] = stock
        # DESKHERO
        elif 'productitem' in productClass:
            logger.debug(f"{vendor.name} productitem")
            productArray['url'] = product.find('a').get('href')
            productArray['name'] = product.find(class_='productitem--title').a.contents[0]
        # TheKeyCompany
        elif 'grid-product__grid-item' in productClass:
            logger.debug(f"{vendor.name} grid-product__grid-item")
            # URL
            productArray['url'] = product.find('a').get('href')
            # Name
            productArray['name'] = product.find(class_='grid-product__title').contents[0]
            # Image
            productArray['image'] = product.find(class_='grid-product__image').get('src')
            # Price and stock
            priceTag = product.find(class_='grid-product__price')
            if priceTag:
                price = priceFormat.search(priceTag.contents[0])[0]
            else:
                price = "0.00"
            productArray['price'] = price
            stockCheck = product.find(class_='grid-product__status-bar').contents
            if "Sold Out" in stockCheck or "Coming Soon" in stockCheck:
                stock = False
            else:
                stock = True
            productArray['stock'] = stock
        # MKUltra
        elif 'product' in productClass:
            logger.debug(f"{vendor.name} product")
            # URL
            productArray['url'] = product.find('a').get('href')
            # Name
            productArray['name'] = product.find(class_='product__title').a.contents[0]
            # Image
            if imageClass := product.find(class_='product__image'):
                if imageDataSrc := imageClass.get('data-src'):
                    image = imageDataSrc.format(width=2048)
            elif imageClass := product.find(class_='product__image-wrapper'):
                image = imageClass.img.get('src')
            productArray['image'] = image
            # Price and stock
            priceClass = product.find(class_='product__price')
            if priceClass:
                if len(priceClass.contents) == 1:
                    price = priceFormat.search(priceClass.contents[0])[0]
                else:
                    price = priceFormat.search(priceClass.contents[2])[0]
            productArray['price'] = price
            stockClass = product.find(class_='sold-out-text')
            if stockClass:
                stock = False
            else:
                stock = True
            price = 'product__price'
            productArray['stock'] = stock
        # Switchmod
        elif 'product-grid-item' in productClass:
            logger.debug(f"{vendor.name} product-grid-item")
            # URL
            productArray['url'] = product.get('href')
            # Name
            productArray['name'] = product.p.contents[0]
            # Image
            productArray['image'] = product.find(class_='lazyload__image-wrapper').img.get('data-src').format(width=2048)
            # Price and stock
            productArray['price'] = priceFormat.search(product.find(class_='product-item--price').small.contents[0])[0]
            productArray['stock'] = True if not product.find(class_='badge--sold-out') else False
        else:
            print("Big issues!")
        # Name filtering should be done down here to remove characters like `\n` and spaces from the start and end of the name
        prodDict.append(productArray)
    return prodDict
