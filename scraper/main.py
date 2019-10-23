#!/usr/bin/env python3
#standard modules
import json, asyncio

#My custom modules
import vendors

#CMS list
import cms.shopify.shopify

vendors = []

cms = []

async def main():
    await loadVendors()
    await loadCMS()
    for vendor in vendors:
        print(vendor['cms'])

async def loadCMS():
    global cms
    with open('cms.json', 'r') as f:
        cms = json.load(f)

asyncio.run(main())
