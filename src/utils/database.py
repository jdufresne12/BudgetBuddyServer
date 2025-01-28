import asyncpg
from typing import Optional

class Database:
   pool: Optional[asyncpg.Pool] = None

   @classmethod
   async def connect(cls):
       if not cls.pool:
           cls.pool = await asyncpg.create_pool(
               user='your_user',
               password='your_password',
               database='your_db',
               host='localhost'
           )
       return cls.pool