import aiohttp
import asyncio

async def fetch(client):
    url = 'http://localhost:8080/'
    data={}
    data["text"] = "abcde"
    async with client.post(url,data=data) as resp:
          return await resp.text()

async def main(loop):
    async with aiohttp.ClientSession(loop=loop) as client:
        html = await fetch(client)
        print(html)

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))