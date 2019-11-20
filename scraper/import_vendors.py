import configparser, json, crawl, vendormanage, elasticsearch, asyncio

config = configparser.ConfigParser()
config.read('config/elastic.ini')

url = config['elastic']['url']

es = elasticsearch.ElasticSearch(url)
vendors = vendormanage.load_vendors()

index = "vendors/"

endpoint = f"{index}vendor/"

returneddata = asyncio.run(crawl.crawl(f"{url}{index}", 'PUT'))

print(json.loads(returneddata))

for vendor in vendors:
    vendor_endpoint = f"{endpoint}{vendor['uuid']}"
    vendor_returneddata = asyncio.run(es.store(vendor_endpoint, vendor))
    print(json.loads(vendor_returneddata))
