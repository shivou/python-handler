import os
import requests
from aiohttp import web
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
hostName = config.get('server', 'ip')
hostPort = config.getint('server', 'port')

async def handler(request):
    body = await request.post()
    response = requests.post(os.environ['RTMP_URL']+request.match_info['name'], data=body)
    try:
        content = response.json()
    except ValueError:
        content = response.content
    if "data" in content and "path" in content['data']:
        return web.HTTPTemporaryRedirect(content['data']['path'])
    return web.Response(status=response.status_code)

app = web.Application()
app.add_routes([web.post('/{name}', handler)])

web.run_app(app, host=hostName, port=hostPort)
