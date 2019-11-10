#!/usr/bin/env python3
# standard modules
import json, asyncio, logging, sys, argparse
from configparser import ConfigParser

# My custom modules
from base_vendors import Vendor, load_vendors
from base_cms import CMS
from crawl import crawl

config = ConfigParser()
config.read('config/cms.ini')

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

log_format = '%(asctime)s %(levelname)s %(filename)s %(message)s'
log_date_format = '[%d-%m-%Y %H:%M:%S]'

formatter = logging.Formatter(log_format, datefmt=log_date_format)
file_handler = logging.FileHandler('log/scraper.main.log', mode='w')
stdout_handler = logging.StreamHandler(sys.stdout)

logger = logging.getLogger('scraper_main')

file_handler.setFormatter(formatter)
stdout_handler.setFormatter(formatter)

logger.setLevel(logging.DEBUG)

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)

vendors = []

vendors = load_vendors()

vendor_objects = []

def main():
    logger.debug('main()')
    for vendor in vendors:
        cms_object = None
        vendor_object = None
        if vendor['scrape'] and config[vendor['cms']]['scrape']:
            cms_object = CMS(vendor).cms
            vendor_object = Vendor(vendor)
            cms_object.vendor = vendor_object
            vendor_object.cms = cms_object
            vendor_objects.append(vendor_object)
        else:
           logger.debug(f"Vendor {vendor['name']} not loaded.")
    asyncio.run(parse_vendors())

async def parse_vendors():
    for vendor in vendor_objects:
        logger.debug(f"Started {vendor.name}.")
        await vendor.cms.load()
        logger.debug(f"Loaded {vendor.name}. {len(vendor.cms.products)} products loaded. Parsing.")
        await vendor.cms.parse()
        logger.debug(f"Completed {vendor.name}. {len(vendor.products)} products parsed.")
main()
