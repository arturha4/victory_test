import asyncpg

from asyncpg.pool import Pool

from config import (
    PG_USER,
    PG_PASSWORD,
    PG_DB,
    PG_HOST,
    PG_PORT
)

class PgAsyncConn:
     def __init__(self):
        self._pool = None

     async def init_db_pool(self):
        if self._pool is None:
            self._pool = await asyncpg.create_pool(
                 user=PG_USER,
                 password=PG_PASSWORD,
                 database=PG_DB,
                 host=PG_HOST,
                 port=PG_PORT
            )

     async def close_db_pool(self):
         if self._pool:
             await self._pool.close()
             _pool = None

     async def get_db_pool(self) -> Pool:
         if self._pool is None:
             raise Exception("Pool is not initialized, call init_db_pool first")
         return self._pool

     async def query(self):
        async with self._pool.acquire() as conn:
            version = await conn.fetchval('SELECT version()')
            print(f"Подключено к: {version}")
