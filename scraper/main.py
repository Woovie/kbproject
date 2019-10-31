#!/usr/bin/env python3
#standard modules
import json, asyncio, logging, os, sys

#My custom modules
import baseVendors, baseCMS

#CMS list
import cms.shopify.main

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

def main():
    logger.debug('main()')
    for vendor in vendors:
        ven = baseVendors.vendor(vendor['vendorName'], vendor['vendorURL'], vendor['cms'], vendor['scrape'])#name, url, cms, active
        logger.debug(f"Loaded \"{ven.name}\" at \"{ven.url}\"")

main()
