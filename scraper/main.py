#!/usr/bin/env python3
#standard modules
import json, asyncio, logging, os, sys, timeit

#My custom modules
import baseVendors, baseCMS
from crawl import crawl

#CMS list
from cms.shopify.main import shopify, loadProducts

logFormat = '%(asctime)s %(levelname)s %(filename)s %(message)s'
logDateFormat = '[%d-%m-%Y %H:%M:%S]'

formatter = logging.Formatter(logFormat, datefmt=logDateFormat)
fileHandler = logging.FileHandler('scraper.main.log', mode='w')
stdoutHandler = logging.StreamHandler(sys.stdout)

logger = logging.getLogger('scraperMain')

fileHandler.setFormatter(formatter)
stdoutHandler.setFormatter(formatter)

logger.setLevel(logging.DEBUG)

logger.addHandler(fileHandler)
logger.addHandler(stdoutHandler)

vendors = []
cms = []

vendors = baseVendors.loadVendors()
cms = baseCMS.loadCMS()

vendorObjects = []

def main():
    logger.debug('main()')
    for vendor in vendors:
        cms = None
        if vendor['cms'] == 'shopify':
            cms = shopify(vendor['vendorURL'])
        ven = baseVendors.vendor(vendor['vendorName'], vendor['vendorURL'], cms, vendor['scrape'], vendor['dataName'])#name, url, cms, active
        vendorObjects.append(ven)
    asyncio.run(parseVendors())

async def parseVendors():
    for vendor in vendorObjects:
        if vendor.active:
            logger.debug(f"Started {vendor.name} at {vendor.url}.")
            await vendor.cms.parseStorePage(f"{vendor.url}{vendor.cms.firstURI}")
            vendor.products = await loadProducts(vendor)
            logger.debug(f"Finished {vendor.name}, loaded {len(vendor.products)} products.")
            with open(f"{vendor.dataName}.json", 'w') as outfile:
                json.dump(vendor.products, outfile)
            logger.debug(f"Wrote {vendor.name} data to {vendor.dataName}.json")
main()
