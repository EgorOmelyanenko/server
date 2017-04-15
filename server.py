import asyncio, time, ssl, pathlib,json
from aiohttp import web # ставил pip3 install aiohttp
import db_log, sdk
import JsonDataBase as jdb

class Server(asyncio.Protocol):
    #OK
    async def req_post(request):  # обработчик запроса POST

        print('connected, operation = POST')
        params = request.query
        print (request.method, params)

        if  params['operation']=='add_profile':
            #params_text = params['text']
            per = sdk.add_profile(name=params['name'],birth=params['birth'],
                                  tag=params['tag'], gender=params['gender'])
            id_user = per.pop('result')
            error= per.pop('error')
            jdb.AddInfo(id=id_user,name=params['name'],birth=params['birth'],
                        tag=params['tag'], gender=params['gender'])
            db_log.other_operation(params['operation'],error=error,id_user=str(id_user))
            return web.json_response(error)

        elif params['operation']=='ident_profile':
            data=await request.read()
            file=open(r'srvimg/img.jpg','wb')
            file.write(data)
            rtrn = sdk.ident_profile()
            db_log.other_operation(params['operation'], error=rtrn['error'], id_user=str(rtrn['result'][0]['profile_id']))
            if rtrn['error']==0:
                rtrn['score'] = rtrn['result'][0]['score']
                rtrn['result'] = jdb.GetInfo(rtrn['result'][0]['profile_id'])
                rtrn.pop('error')
                return web.json_response(rtrn)
            else:
                return web.json_response('Профиль не распознан')

        else:
            return web.json_response(None)
    #OK
    async def req_put(request):  # обработчик запроса PUT
        params = request.query
        print(request.method, params)
        print(params['operation'])
        rtrn = dict()
        if params['operation'] == 'update_profile':
            if (jdb.GetInfo(params['id']) != None):
                jdb.UpdateInfo(id=params['id'],name=params['name'],birth=params['birth'],
                               tag=params['tag'], gender=params['gender'])
            else:
                jdb.AddInfoid(id=params['id'],name=params['name'],birth=params['birth'],
                tag=params['tag'], gender=params['gender'])
            db_log.other_operation(params['operation'], error=0,id_user=params['id'])
            return web.json_response(rtrn)
        else:
            return web.json_response(None)

    async def req_del(request):  # обработчик запроса DELETE
        params = request.query
        print(request.method, params)
        print('connected, method - DELETE')
        id_del = params['id']
        error = sdk.del_profile(id_del)
        if (error!=1):
            jdb.DelInfo(id_del)
        db_log.other_operation(params['operation'],error, id_user=str(id_del))
        return web.json_response(1)
    #OK
    async def req_get(request):  # обработчик запроса GET
        params = request.query

        print(request.method, params)
        if params['operation']=='get_info':
            return web.json_response(jdb.GetInfo(params['text']['id']))
        elif params['operation']=='get_all_id':
            return web.json_response(jdb.GetAllId())

        elif params['operation']=='get_log':
            return web.json_response(db_log.select())

        elif params['operation']=='get_profile_imgs_id':
            return web.json_response(sdk.get_profile_imgs_id(params['text']['id']))

        elif params['operation']=='get_profile_imgs_id':
            return web.json_response(sdk.get_profile_imgs_id(params['text']['id']))

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
    server_coro = loop.create_server(app.make_handler(), 'localhost',8080,ssl=ssl_context)
    server = loop.run_until_complete(server_coro)
    loop.run_forever()
    loop.close()

