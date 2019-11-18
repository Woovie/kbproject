import json, asyncio, configparser, logging

#my modules
import crawl

logger = logging.getLogger('scraper_main')

config = configparser.ConfigParser()
config.read('config/elastic.ini')

class ElasticSearch():
    def __init__(self, url):
        self.url = url
    async def list(self, endpoint = None):
        url = f"{self.url}{endpoint}"
        return await crawl.crawl(url)
    async def store(self, endpoint, data):
        url = f"{self.url}{endpoint}"
        return await crawl.crawl(url, method = 'POST', json = data)
