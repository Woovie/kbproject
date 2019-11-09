import aiohttp
from sys import exit

async def crawl(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 200:
                return await r.text()
            else:
                print(f"[ERROR] GET {url} returned unexpected value: {r.status} {r.reason}, expected 200 OK")
                exit()
