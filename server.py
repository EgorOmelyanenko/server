import asyncio, time, ssl, pathlib
from aiohttp import web # ставил pip3 install aiohttp

class Server(asyncio.Protocol):

    async def req_post(request):  # обработчик запроса
        print ('connected')
        data=await request.post()
        return web.Response(text='hello post'+' '+str(data["text"]).upper())

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

