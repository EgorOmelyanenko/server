import aiohttp,asyncio,json
import ssl,pathlib
async def fetch(client):
    url = 'https://localhost:8080/'
    data={}
    data["text"] = 'select'
    async with client.post(url,data=data) as resp:
          return await resp.text()

async def main(loop):
    here = pathlib.Path(__file__)
    ssl_cert = here.parent / 'server.crt'
    sslcontext = ssl.create_default_context(cafile=str(ssl_cert))
    conn = aiohttp.TCPConnector(ssl_context=sslcontext)
    async with aiohttp.ClientSession(loop=loop,connector=conn) as client:
        html = await fetch(client)
        print(html)
loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))