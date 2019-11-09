import json, crawl 

class vendor():
    def __init__(self, name, url, cms, active, dataName):
        self.products = []
        self.name = name
        self.url = url
        self.cms = cms
        self.active = active
        self.dataName = dataName

def loadVendors():
    with open('config/vendors.json', 'r') as f:
        return json.load(f)
