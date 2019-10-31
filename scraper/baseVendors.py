import json, crawl 

class vendor():
    def __init__(self, name, url, cms, active):
        self.products = []
        self.name = name
        self.url = url
        self.cms = cms
        self.active = active

def loadVendors():
    with open('vendors.json', 'r') as f:
        return json.load(f)
