import aiohttp,asyncio,json
import ssl,pathlib
async def fetch(client):
    url = 'https://localhost:8080/'
    param={}
    param['operation'] = 'delete_profile'
    param.update({'id':'14882','name':'Egor','birth':'29.12.9999', 'tag':'SUPER_PUPER_POMIDOR', 'gender':'m'})
    print (param)
    #POST
    if (param['operation'] == 'add_profile'):
        async with client.post(url,params=param) as resp:
          return await resp.text()
    elif (param['operation'] == 'ident_profile'):
        async with client.post(url,data=open(r'img/737-66.jpg','rb'),params=param) as resp:
          return await resp.text()
    # PUT
    elif (param['operation'] == 'update_profile'):
        async with client.put(url,params=param) as resp:
            return await resp.text()
    # DELETE
    elif (param['operation'] == 'delete_profile'):
        async with client.delete(url,params=param) as resp:
            return await resp.text()
    # GET
    elif (param['operation'] == 'get_info' or 'get_log' or 'get_all_id' or 'get_profile_imgs_id' or 'get_profile_image'):
        async with client.get(url, params=param) as resp:
            return await resp.text()
    else:
        return 'Неправильная операция'


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