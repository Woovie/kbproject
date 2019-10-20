import sys, os, asyncio

shopifyPath = f"{os.path.dirname(os.path.realpath(__file__))}/../cms/shopify"

os.chdir(shopifyPath)
sys.path.insert(1, shopifyPath)

from shopify import shopify

site = 'https://dailyclack.com'

async def main():
    await shopify.crawl()
    await shopify.loadProducts()
    print(shopify.products)

shopify = shopify(site)
asyncio.run(main())
