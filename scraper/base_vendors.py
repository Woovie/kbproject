import json, crawl 

class Vendor():
    def __init__(self, vendor):
        self.products = []
        self.name = vendor['name']
        self.url = vendor['url']
        self.scrape = vendor['scrape']
        self.dataname = vendor['dataname']
        self.uuid = vendor['uuid']
        self.cms = None

def load_vendors():
    with open('config/vendors.json', 'r') as f:
        return json.load(f)

def save_vendors(vendors):
    with open('config/vendors.json', 'w') as f:
        json.dump(vendors, f)
