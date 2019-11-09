#!/usr/bin/env python3
# standard modules
import json, asyncio, logging, sys, argparse

# My custom modules
import baseVendors, baseCMS
from crawl import crawl

# CMS list
from cms.shopify.main import shopify, loadProducts

# Description
desc = '''
CMS Scraper

-h, --help      Display this text
-v, --verbose   Output debug messages

scraper 

'''

parser = argparse.ArgumentParser()

parser.add_argument('-v', '--verbose', help="Output debug messages")

arguments = parser.parse_args()

logFormat = '%(asctime)s %(levelname)s %(filename)s %(message)s'
logDateFormat = '[%d-%m-%Y %H:%M:%S]'

formatter = logging.Formatter(logFormat, datefmt=logDateFormat)
fileHandler = logging.FileHandler('log/scraper.main.log', mode='w')
stdoutHandler = logging.StreamHandler(sys.stdout)

logger = logging.getLogger('scraperMain')

fileHandler.setFormatter(formatter)
stdoutHandler.setFormatter(formatter)

logger.setLevel(logging.DEBUG)

logger.addHandler(fileHandler)
logger.addHandler(stdoutHandler)

if arguments.verbose:
    logger.debug("Debug mode enabled!")

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
            if len(vendor.cms.products) > 0:
                vendor.products = await loadProducts(vendor)
                logger.debug(f"Finished {vendor.name}, loaded {len(vendor.products)} products.")
                with open(f"datastore/{vendor.dataName}.json", 'w') as outfile:
                    json.dump(vendor.products, outfile)
                logger.debug(f"Wrote {vendor.name} data to datastore/{vendor.dataName}.json")
            else:
                logger.debug(f"Finished {vendor.name}, no products found.")
main()
