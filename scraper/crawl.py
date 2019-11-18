import aiohttp, logging

logger = logging.getLogger('scraperMain')

valid_methods = [
        'POST',
        'PATCH',
        'PUT'
        'GET',
        'DELETE',
        'OPTIONS',
        'HEAD'
]

async def crawl(url, request = None, payload = None, json = None):
    async with aiohttp.ClientSession() as session:
        if request in valid_methods or not request:
            method = request if request else 'GET'
            async with session.request(method, url, data = payload, json = json) as r:
                return await process_return(r)
        else:
            logger.error(f"Request type {request} is invalid.")
            return False

async def process_return(request_object):
    if request_object.status < 400:#Normal
        return await request_object.text()
    else:
        logger.error(f"{request_object.url} returned {request_object.status} {request_object.reason}")
        return False
