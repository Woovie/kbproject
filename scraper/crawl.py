import aiohttp, logging

logger = logging.getLogger('scraperMain')

valid_methods = [
        'POST',
        'PATCH',
        'PUT',
        'GET',
        'DELETE',
        'OPTIONS',
        'HEAD'
]

async def crawl(url, method = None, payload = None, json = None):
    async with aiohttp.ClientSession() as session:
        if method in valid_methods or not method:
            method = method if method else 'GET'
            async with session.request(method, url, data = payload, json = json) as r:
                return await process_return(r)
        else:
            return False

async def process_return(request_object):
    if request_object.status < 400:#Normal
        return await request_object.text()
    else:
        return await request_object.text()
