import json, crawl, 

class vendor():
    def __init__(self, name, url, cms, active):
        self.products = []
        self.name = name
        self.url = url
        self.cms = cms
        self.active = active
    async def initCrawl(self):
        if self.active:
            return True

async def loadVendors():
    global vendors
    with open('vendors.json', 'r') as f:
        vendors = json.load(f)
