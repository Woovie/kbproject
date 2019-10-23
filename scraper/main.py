#!/usr/bin/env python3
#standard modules
import json, asyncio

#My custom modules
import baseVendors, baseCMS

#CMS list
import cms.shopify.main

vendors = []

cms = []

async def main():
    global vendors
    global cms
    vendors = await baseVendors.loadVendors()
    cms = await baseCMS.loadCMS()
    for vendor in vendors:
        ven = baseVendors.vendor(vendor['vendorName'], vendor['vendorURL'], vendor['cms'], vendor['scrape'])#name, url, cms, active


asyncio.run(main())
