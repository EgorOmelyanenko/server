import asyncio, time, ssl, pathlib,json
from aiohttp import web # ставил pip3 install aiohttp
from db import *

class Server(asyncio.Protocol):

    async def req_post(request):  # обработчик запроса

        data=await request.post()
        print('connected, data = ' + str(data["text"]))

        rtrn=dict()
        if data["text"]=="select":
            sel_res=select()
            i=1
            for r in sel_res:
                rtrn[i]={"id_log":r[0], "id_user":r[1],"result":r[2],"may":r[3],"action":r[4]}
                i=i+1
        else:
            sel_res=other_operation(data["text"])

        return web.json_response(rtrn)

if __name__ == "__main__":
    app = web.Application()  
    app.router.add_post('/', Server.req_post) #разрешаем метод POST
    loop = asyncio.get_event_loop()
    #ssl
    here = pathlib.Path(__file__)
    ssl_cert = here.parent / 'server.crt'
    ssl_key = here.parent / 'server.key'
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(str(ssl_cert), str(ssl_key))
    #ssl
    server_coro = loop.create_server(app.make_handler(), 'localhost',8080,ssl=ssl_context)
    server = loop.run_until_complete(server_coro)
    loop.run_forever()
    loop.close()

