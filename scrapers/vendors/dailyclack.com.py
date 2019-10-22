import sys, os, asyncio, json

originalPath = os.path.dirname(os.path.realpath(__file__))
shopifyPath = f"{os.path.dirname(os.path.realpath(__file__))}/../cms/shopify"

os.chdir(shopifyPath)
sys.path.insert(1, shopifyPath)

from shopify import shopify, crawl

companyName = 'Daily Clack'
site = 'https://dailyclack.com'
referralCode = ''

async def main():
    print(f"Starting product parse for {companyName}")
    await shopify.parseStorePage(f"{shopify.site}{shopify.initStoreURI}")
    await shopify.loadProducts()
    json.dumps(shopify.products, indent=4)
    os.chdir(originalPath)
    with open('dailyclack.com.json', 'w') as writeout:
        json.dump(shopify.products, writeout, indent=4)
    print(f"Complete!")

shopify = shopify(site)
asyncio.run(main())
