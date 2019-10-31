import json, crawl 

def loadCMS():
    with open('cms.json', 'r') as f:
        return json.load(f)
