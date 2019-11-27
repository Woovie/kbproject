import json, asyncio, logging

#my modules
import crawl

logger = logging.getLogger('scraper_main')

class ElasticSearch():
    def __init__(self, url):
        self.url = url
    async def list(self, endpoint = None):
        url = f"{self.url}{endpoint or ''}"
        return await crawl.crawl(url)
    async def store(self, endpoint, data):
        url = f"{self.url}{endpoint}"
        return await crawl.crawl(url, method = 'POST', json = data)
