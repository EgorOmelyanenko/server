import asyncio,aiopg
from sqlalchemy import *


dsn = 'dbname=log_db user=postgres password=1234 host=localhost'

'''
async def test_select():
    async with aiopg.create_pool(dsn) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * from log")
                ret = []
                async for row in cur:
                    ret.append(row)
                assert ret == [(1,)]
    print("ALL DONE")


loop = asyncio.get_event_loop()
loop.run_until_complete(test_select())
'''
import json
def select():
    engine = create_engine('postgresql://postgres:1234@localhost:5432/log_db')
    result = engine.execute("select * from log;")
    return result

