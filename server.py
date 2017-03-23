import asyncio, time
from aiohttp import web # ставил pip3 install aiohttp

class Server(asyncio.Protocol):

    async def req_post(request):  # обработчик запроса
        data=await request.post()
        return web.Response(text='hello post'+' '+str(data["text"]).upper())

if __name__ == "__main__":
    app = web.Application()  
    app.router.add_post('/', Server.req_post) #разрешаем метод POST
    loop = asyncio.get_event_loop()
    server_coro = loop.create_server(app.make_handler(), 'localhost',8080)
    server = loop.run_until_complete(server_coro)
    loop.run_forever()
    loop.close()

