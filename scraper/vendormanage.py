import json, re, uuid

url_pattern = re.compile(r"https://(.*)\.(.*)")

def load_vendors():
    with open('config/vendors.json', 'r') as f:
        return json.load(f)

def save_vendors(vendors):
    with open('config/vendors.json', 'w') as f:
        json.dump(vendors, f)

def add_vendor(name, url, cms, active, currency = False):
    vendor = {}
    vendor['name'] = name
    vendor['url'] = url
    dataname_data = re.match(url_pattern, url)
    print(dataname_data)
    vendor['dataname'] = f"{dataname_data.group(1)}_{dataname_data.group(2)}"
    vendor['cms'] = cms
    vendor['scrape'] = bool(active)
    vendor['currency'] = False
    vendor['uuid'] = str(uuid.uuid5(uuid.NAMESPACE_DNS, vendor['url']))
    vendors = load_vendors()
    vendors.append(vendor)
    save_vendors(vendors)
