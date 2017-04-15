import asyncio, time, ssl, pathlib,json
from aiohttp import web # ставил pip3 install aiohttp
import db_log, sdk
import JsonDataBase as jdb

class Server(asyncio.Protocol):

    async def req_post(request):  # обработчик запроса POST

        data=await request.post()
        data_body=eval(data['text'])

        print('connected, operation = ' + str(data["operation"]) + ', data =' + str(data_body) )

        rtrn=dict()
        if  data['operation']=="add_profile":
            per = sdk.add_profile(name=data_body['name'],birth=data_body['birth'],
                                  tag=data_body['tag'], gender=data_body['gender'])
            id_user = per.pop('result')
            jdb.AddInfo(id=id_user,name=data_body['name'],birth=data_body['birth'],
                        tag=data_body['tag'], gender=data_body['gender'])
            db_log.other_operation(data['operation'],error=per.pop('error'),id_user=str(id_user))


        return web.json_response(rtrn)

    async def req_put(request):  # обработчик запроса PUT
        data = await request.post()
        print(request.url)
        data_body = eval(data['text'])

        print('connected, operation = ' + str(data["operation"]) + ', data =' + str(data_body))

        rtrn = dict()
        if data['operation'] == "update_profile":
            if (jdb.GetInfo(data_body['id']) != None):
                jdb.UpdateInfo(id=data_body['id'],name=data_body['name'],birth=data_body['birth'],
                               tag=data_body['tag'], gender=data_body['gender'])
            else:
                jdb.AddInfoid(id=data_body['id'],name=data_body['name'],birth=data_body['birth'],
                tag=data_body['tag'], gender=data_body['gender'])
            db_log.other_operation(data['operation'], error=0,id_user=str(data_body['id']))

        return web.json_response(rtrn)

    async def req_del(request):  # обработчик запроса DELETE
        data = dict(await request.post())
        print(data)
        print('connected, method - DELETE')
        id_del = eval(data['text'])['id']
        error = sdk.del_profile(id_del)
        if (error!=1):
            jdb.DelInfo(id_del)
        db_log.other_operation(data['operation'],error, id_user=str(id_del))
        return web.json_response()

    async def req_get(request):  # обработчик запроса GET
        data = request.query
        print(data)
        if data['operation']=='get_info':
            return web.json_response(jdb.GetInfo(data['id']))
        elif data['operation']=='get_all_id':
            return web.json_response(jdb.GetAllId())
        elif data['operation']=='get_log':
            return web.json_response(db_log.select())
        else:
            return web.json_response(None)




if __name__ == "__main__":
    app = web.Application()
    # разрешаем методы
    app.router.add_post('/', Server.req_post)
    app.router.add_get('/', Server.req_get)
    app.router.add_put('/', Server.req_put)
    app.router.add_delete('/', Server.req_del)
    loop = asyncio.get_event_loop()
    #ssl
    here = pathlib.Path(__file__)
    ssl_cert = here.parent / 'server.crt'
    ssl_key = here.parent / 'server.key'
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(str(ssl_cert), str(ssl_key))
    #ssl
    server_coro = loop.create_server(app.make_handler(), 'localhost',8081,ssl=ssl_context)
    server = loop.run_until_complete(server_coro)
    loop.run_forever()
    loop.close()

