import pprint, sys, json, re, uuid, argparse, base_vendors, base_cms

description = 'Add and remove vendors from the JSON array.'
parser = argparse.ArgumentParser(description=description)
parser.add_argument('--add', help='Add a vendor', nargs=4, metavar=('Vendor name,', 'URL,', 'CMS,', 'Active'))
parser.add_argument('--list', help='List vendors', action='store_true')
parser.add_argument('--delete', help='Delete a vendor by UUID', metavar='UUID')

args = parser.parse_args()

url_pattern = re.compile(r"https://(www.)?(.*)\.(.*)")

true_booleans = ['y', 'yes', 'true', '1']
false_booleans = ['n', 'no', 'false', '0']

def main():
    #Namespace(add=['Dixie Mech', 'https://google.com', 'Shopify', 'true'], list=False)
    if args.add:
        dataname_data = re.match(url_pattern, args.add[1])
        vendor = {
            'name': args.add[0],
            'url': args.add[1],
            'dataname': f"{dataname_data.group(2)}_{dataname_data.group(3)}",
            'cms': args.add[2],
            'active': args.add[3]
        }
        vendor['active'] = bool_convert(vendor['active'])
        vendors = base_vendors.load_vendors()
        cmss = base_cms.load_cms()
        if vendor['name'].lower() in [_vendor['name'] for _vendor in vendors]:
            print(f"Vendor {vendor['name']} already exists.")
            sys.exit()
        if vendor['url'].lower() in [_vendor['url'] for _vendor in vendors]:
            print(f"Vendor {vendor['url']} already exists.")
            sys.exit()
        if vendor['url'].endswith('/'):
            print(f"The vendor URL should not end with /, please modify the URL.")
            sys.exit()
        if not vendor['cms'].lower() in [cms['name'] for cms in cmss]:
            print(f"CMS {vendor['cms']} is not a valid CMS. Does it exist?")
            sys.exit()
        if type(vendor['active']) != bool:
            print(f"Active must be a boolean in the form of the following options:")
            print(true_booleans+false_booleans)
            sys.exit()
        vendor_as_string
        print(f"Adding vendor: {pprint.pprint(vendor)}")
        verify = verify_prompt("Is everything correct?")
        if verify:
            print("Adding vendor...")
            add_vendor(vendor['name'], vendor['url'], vendor['cms'].lower(), vendor['active'])
            print("Added.")
        else:
            print("Aborting.")
            sys.exit()
    if args.list:
        print(get_vendors_in_json())
    if args.delete:
        uuid = args.delete
        vendors = base_vendors.load_vendors()
        vendor_in_dict = value_in_dict(vendors, uuid)
        if not vendor_in_dict:
            print("Vendor does not exist. Check vendor list to ensure the UUID provided matches.")
            sys.exit()
        else:
            print("Vendor to delete:")
            print(pprint.pprint(vendor_in_dict))
            verify = verify_prompt("Is everything correct?")
            if verify:
                print("Deleting vendor...")
                delete_vendor(uuid)
                print("Vendor deleted.")
            else:
                print("Aborting.")
                sys.exit()

def add_vendor(name, url, cms, active, currency = False):
    vendor = {}
    vendor['name'] = name
    vendor['url'] = url
    dataname_data = re.match(url_pattern, url)
    vendor['dataname'] = f"{dataname_data.group(2)}_{dataname_data.group(3)}"
    vendor['cms'] = cms
    vendor['scrape'] = bool(active)
    vendor['currency'] = False
    vendor['uuid'] = str(uuid.uuid5(uuid.NAMESPACE_DNS, vendor['url']))
    vendors = base_vendors.load_vendors()
    vendors.append(vendor)
    base_vendors.save_vendors(vendors)

def delete_vendor(uuid):
    vendors = base_vendors.load_vendors()
    vendors = [vendor for vendor in vendors if not (vendor.get('uuid') == uuid)]
    base_vendors.save_vendors(vendors)

def get_vendors_in_json():
    vendors = base_vendors.load_vendors()
    return json.dumps(vendors, indent=4)

#Utility
def bool_convert(boolable):
    if boolable in true_booleans:
        return True
    if boolable in false_booleans:
        return False
    return None

def verify_prompt(question):
    reply = str(input(f"{question} y/n\n")).lower()
    return bool_convert(reply[:1])

def value_in_dict(dict_list, value):
    for dict_obj in dict_list:
        if value in dict_obj.values():
            return dict_obj
    return False

main()
