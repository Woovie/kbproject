import json, crawl 

def loadCMS():
    with open('config/cms.json', 'r') as f:
        return json.load(f)
