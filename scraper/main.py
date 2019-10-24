#!/usr/bin/env python3
#standard modules
import json, asyncio, logging, os, logging

#My custom modules
import baseVendors, baseCMS

#CMS list
import cms.shopify.main

vendors = []

cms = []

async def main():
    logger.critical('test')
    global vendors
    global cms
    vendors = await baseVendors.loadVendors()
    cms = await baseCMS.loadCMS()
    for vendor in vendors:
        ven = baseVendors.vendor(vendor['vendorName'], vendor['vendorURL'], vendor['cms'], vendor['scrape'])#name, url, cms, active

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s %(levelname)s %(filename)s %(message)s',
                    datefmt='[%d-%m-%Y %H:%M:%S]',
                    filename='debug.log',
                    filemode='w')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

asyncio.run(main())
