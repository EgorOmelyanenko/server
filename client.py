import aiohttp,asyncio,json
import ssl,pathlib
async def fetch(client):
    url = 'https://localhost:8081/'
    data={}
    data['operation'] = 'select'
    data['text']=str({'id':'14899','name':'Egor','birth':'29.12.9999', 'tag':'EGOR_SUPER_POMIDOR', 'gender':'m'})
    kwargs = {'123':'123'}
    #в зависимости от операции вызываем нужный метод
    if (data["operation"] == 'add_profile'):
        async with client.post(url,data=data) as resp:
          return await resp.text()
########################################
    elif (data["operation"] == 'get_profile_info'):
        par={'id':14899}
        async with client.get(url, params = par) as resp:
            print(resp.url)
            return await resp.text()
 #######################################
    elif (data["operation"] == 'select'):
            async with client.get(url) as resp:
                       return await resp.text()

    elif (data["operation"] == 'update_profile'):
        async with client.put(url,data=data) as resp:
            print(resp.url)
            return await resp.text()
    elif (data["operation"] == 'delete_profile'):
        async with client.delete(url,data=data) as resp:
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