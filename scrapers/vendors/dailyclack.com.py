import sys, os, asyncio

shopifyPath = f"{os.path.dirname(os.path.realpath(__file__))}/../cms/shopify"

os.chdir(shopifyPath)
sys.path.insert(1, shopifyPath)

from shopify import shopify

companyName = 'Daily Clack'
site = 'https://dailyclack.com'
referralCode = ''

async def main():
    await shopify.crawl()
    await shopify.loadProducts()
    for entry in shopify.resp.entries:
        print(entry.title.value)

shopify = shopify(site)
asyncio.run(main())
